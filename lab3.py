import json
from pathlib import Path

ADMIN_PASSWORD = "admin123"
STOCK_FILE = Path(__file__).with_name("stock_data.json")

DEFAULT_PRODUCTS = [
    {"id": 1, "name": "Механічна клавіатура", "price": 1850.0, "stock": 8},
    {"id": 2, "name": "Ігрова миша", "price": 949.5, "stock": 14},
    {"id": 3, "name": "Килимок XL", "price": 420.0, "stock": 4},
    {"id": 4, "name": "Навушники дротові", "price": 1299.9, "stock": 3},
    {"id": 5, "name": "USB-хаб 4 порти", "price": 560.25, "stock": 10},
]

# Лямбда-функції для форматування ціни та підрахунку вартості
format_price = lambda amount: f"{amount:.2f}грн"
line_total = lambda price, qty: price * qty


class Product:
    def __init__(self, product_id: int, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def can_supply(self, qty: int) -> bool:
        return 0 < qty <= self.stock

    def reduce_stock(self, qty: int) -> None:
        if not self.can_supply(qty):
            raise ValueError(f"Недостатньо залишку для товару '{self.name}'.")
        self.stock -= qty

    def to_dict(self) -> dict:
        return {
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
        }


class Cart:
    def __init__(self):
        # product_id -> кількість у кошику
        self.items: dict[int, int] = {}

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def add_item(self, product: Product, qty: int) -> tuple[bool, str]:
        if qty <= 0:
            return False, "Кількість має бути більшою за 0."

        current_qty = self.items.get(product.product_id, 0)
        if current_qty + qty > product.stock:
            available_more = product.stock - current_qty
            return (
                False,
                f"Недостатньо товару на складі. Доступно ще: {available_more} шт.",
            )

        self.items[product.product_id] = current_qty + qty
        return True, f"Додано до кошика: {product.name} ({qty} шт.)."

    def remove_item(self, product: Product, qty_to_remove: int) -> tuple[bool, str]:
        prod_id = product.product_id
        if prod_id not in self.items:
            return False, "Цього товару немає у кошику."

        if qty_to_remove <= 0:
            return False, "Кількість має бути більшою за 0."

        current_qty = self.items[prod_id]
        if qty_to_remove >= current_qty:
            del self.items[prod_id]
            return True, f"Товар '{product.name}' повністю видалено з кошика."

        self.items[prod_id] = current_qty - qty_to_remove
        return (
            True,
            f"Зменшено кількість '{product.name}' до {self.items[prod_id]} шт.",
        )

    def calculate_total(self, products: dict[int, Product]) -> float:
        totals = map(
            lambda pair: line_total(products[pair[0]].price, pair[1]),
            self.items.items(),
        )
        return sum(totals)

    def clear(self) -> None:
        self.items.clear()


class Store:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.products: dict[int, Product] = {}
        self.load_stock()

    def load_stock(self) -> None:
        if not self.storage_path.exists():
            self._populate_default_products()
            self.save_stock()
            return

        try:
            raw_data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            if not isinstance(raw_data, list) or not raw_data:
                raise ValueError("Порожній або некоректний формат файлу залишків.")

            self.products.clear()
            for item in raw_data:
                prod = Product(
                    product_id=item["id"],
                    name=item["name"],
                    price=item["price"],
                    stock=item["stock"],
                )
                self.products[prod.product_id] = prod
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            self._populate_default_products()
            self.save_stock()

    def _populate_default_products(self) -> None:
        self.products = {
            item["id"]: Product(item["id"], item["name"], item["price"], item["stock"])
            for item in DEFAULT_PRODUCTS
        }

    def save_stock(self) -> None:
        data = [prod.to_dict() for prod in self.products.values()]
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def sorted_products(self) -> list[Product]:
        return sorted(self.products.values(), key=lambda p: p.price)

    def low_stock_products(self, threshold: int = 5) -> list[Product]:
        return list(filter(lambda p: p.stock < threshold, self.products.values()))

    def checkout(self, cart: Cart) -> tuple[bool, str]:
        if cart.is_empty():
            return False, "Кошик порожній, нічого купувати."

        for prod_id, qty in cart.items.items():
            product = self.products.get(prod_id)
            if product is None or not product.can_supply(qty):
                name = product.name if product else f"ID {prod_id}"
                return False, f"Помилка: для '{name}' не вистачає залишків на складі."

        total = cart.calculate_total(self.products)

        for prod_id, qty in cart.items.items():
            self.products[prod_id].reduce_stock(qty)

        self.save_stock()
        cart.clear()
        return (
            True,
            f"Дякуємо за покупку! Сплачено: {format_price(total)}. Залишки збережено у файл.",
        )


class StoreApp:
    def __init__(self, store: Store, admin_password: str):
        self.store = store
        self.cart = Cart()
        self.admin_password = admin_password

    def show_catalog(self) -> None:
        print("\n--- КАТАЛОГ ТОВАРІВ ---")
        for prod in self.store.sorted_products():
            print(
                f"[{prod.product_id}] {prod.name} | "
                f"Ціна: {format_price(prod.price)} | Наявно: {prod.stock} шт."
            )

    def show_cart(self) -> float:
        print("\n--- ВАШ КОШИК ---")
        if self.cart.is_empty():
            print("Кошик порожній.")
            return 0.0

        for prod_id, qty in self.cart.items.items():
            prod = self.store.products[prod_id]
            subtotal = line_total(prod.price, qty)
            print(
                f"[{prod.product_id}] {prod.name} | {qty} шт. x "
                f"{format_price(prod.price)} = {format_price(subtotal)}"
            )

        total = self.cart.calculate_total(self.store.products)
        print(f"Разом до сплати: {format_price(total)}")
        return total

    def handle_add_to_cart(self) -> None:
        self.show_catalog()
        try:
            prod_id = int(input("\nВведіть ID товару для додавання в кошик: "))
            product = self.store.products.get(prod_id)
            if product is None:
                print("Товар з таким ID не знайдено.")
                return

            qty = int(input("Введіть кількість: "))
            ok, message = self.cart.add_item(product, qty)
            print(message)
        except ValueError:
            print("Помилка: введіть коректне ціле число.")

    def handle_remove_from_cart(self) -> None:
        if self.cart.is_empty():
            print("\nКошик порожній.")
            return

        self.show_cart()
        try:
            prod_id = int(input("\nВведіть ID товару для видалення з кошика: "))
            product = self.store.products.get(prod_id)
            if product is None or prod_id not in self.cart.items:
                print("Цього товару немає у кошику.")
                return

            current_qty = self.cart.items[prod_id]
            qty_to_remove = int(
                input(f"Скільки штук прибрати (у кошику {current_qty} шт.): ")
            )
            ok, message = self.cart.remove_item(product, qty_to_remove)
            print(message)
        except ValueError:
            print("Помилка: введіть коректне ціле число.")

    def handle_checkout(self) -> None:
        if self.cart.is_empty():
            print("\nКошик порожній, нічого купувати.")
            return

        self.show_cart()
        confirm = input("\nПідтвердити покупку? (так/ні): ").strip().lower()
        if confirm not in ("так", "yes", "y", "+"):
            print("Покупку скасовано.")
            return

        ok, message = self.store.checkout(self.cart)
        print(f"\n{message}")

    def handle_admin_panel(self) -> None:
        password = input("\nВведіть пароль адміністратора: ")
        if password != self.admin_password:
            print("Невірний пароль. Доступ заборонено.")
            return

        print("\n--- ПАНЕЛЬ АДМІНІСТРАТОРА: ЗАЛИШКИ НА СКЛАДІ ---")
        for prod in self.store.products.values():
            print(
                f"[{prod.product_id}] {prod.name} | Залишок: {prod.stock} шт. | "
                f"Ціна: {format_price(prod.price)}"
            )

        low_stock = self.store.low_stock_products(threshold=5)
        print("\nТовари з низьким залишком (менше ніж 5 шт.):")
        if low_stock:
            for prod in low_stock:
                print(f"  - {prod.name}: {prod.stock} шт.")
        else:
            print("  Усіх товарів достатньо.")

    def run(self) -> None:
        while True:
            print("\n=== МІНІМАГАЗИН (ООП) ===")
            print("1. Переглянути каталог товарів")
            print("2. Додати товар у кошик")
            print("3. Видалити товар з кошика")
            print("4. Переглянути кошик та купити")
            print("5. Увійти як адміністратор (залишки)")
            print("0. Вийти")

            choice = input("Оберіть дію: ").strip()

            if choice == "1":
                self.show_catalog()
            elif choice == "2":
                self.handle_add_to_cart()
            elif choice == "3":
                self.handle_remove_from_cart()
            elif choice == "4":
                self.handle_checkout()
            elif choice == "5":
                self.handle_admin_panel()
            elif choice == "0":
                print("До побачення!")
                break
            else:
                print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    store = Store(STOCK_FILE)
    app = StoreApp(store=store, admin_password=ADMIN_PASSWORD)
    app.run()