import qrcode


def run_qrcode_demo() -> None:
    qr = qrcode.QRCode(box_size=1, border=1)
    qr.add_data("https://github.com")
    qr.make(fit=True)
    print("[qrcode] QR-код згенеровано (ASCII):")
    qr.print_ascii(invert=True)