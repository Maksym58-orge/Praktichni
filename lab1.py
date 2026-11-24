# 1. Перша програма всіх програмістів
print("Hello, World!")
print("-" * 40)

# 2. Створення змінних різних типів
int_var = 10                      # ціле число (int)
float_var = 3.5                   # дробове число з плаваючою комою (float)
str_var = "Python"                # рядок (str)
bool_var = True                   # логічний тип (bool)
list_var = [1, 2, 3]              # список (list)
tuple_var = (4, 5, 6)             # кортеж (tuple)
set_var = {7, 8, 9}               # множина (set)
dict_var = {"lang": "Python", "ver": 3}  # словник (dict)
none_var = None                   # відсутність значення (NoneType)

variables = [
    int_var, float_var, str_var, bool_var,
    list_var, tuple_var, set_var, dict_var, none_var
]

for var in variables:
    print(f"Значення: {var!r} | Тип: {type(var)}")

print("-" * 40)

# 3. Арифметичні оператори
a = 10
b = 3
print("Додавання (+):", a + b)
print("Віднімання (-):", a - b)
print("Множення (*):", a * b)
print("Ділення (/):", a / b)
print("Цілочисельне ділення (//):", a // b)
print("Остача від ділення (%):", a % b)
print("Піднесення до степеня (**):", a ** b)

# 4. Оператори присвоювання
x = 5
x += 2  # те саме, що x = x + 2
x *= 3  # те саме, що x = x * 3
print("Результат після += та *=:", x)

# 5. Оператори порівняння
print("a == b:", a == b)
print("a != b:", a != b)
print("a > b:", a > b)
print("a < b:", a < b)
print("a >= b:", a >= b)
print("a <= b:", a <= b)

# 6. Логічні оператори (and, or, not)
cond1 = a > 5
cond2 = b > 5
print("cond1 and cond2:", cond1 and cond2)
print("cond1 or cond2:", cond1 or cond2)
print("not cond2:", not cond2)

# 7. Оператори належності (in, not in)
print("'Py' in str_var:", "Py" in str_var)
print("2 in list_var:", 2 in list_var)
print("100 not in list_var:", 100 not in list_var)

# 8. Оператори тотожності (is, is not)
y = None
print("none_var is y:", none_var is y)
print("a is not b:", a is not b)