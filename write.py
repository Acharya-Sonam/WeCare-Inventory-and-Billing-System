import datetime

def write_products(products):
    """
    Overwrite products.txt with updated stock and original cost prices.
    """
    with open("products.txt", "w") as f:
        for p in products:
            country = p.get('country', 'Unknown')
            f.write(f"{p['name']}, {p['brand']}, {p['quantity']}, {p['cost_price']}, {country}\n")


def generate_invoice(data, invoice_type="sale"):
    """
    Build a formatted invoice including 13% VAT, save to a timestamped file, and return both.
    """
    now = datetime.datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S")
    fname = f"{invoice_type}_invoice_{ts}.txt"
    party_label = "Customer" if invoice_type == "sale" else "Vendor"
    party_name  = data.get('customer_name') if invoice_type == "sale" else data.get('vendor_name')
    title       = f"WeCare - {party_label} Invoice"
    lines = [
        "="*50,
        title,
        "="*50,
        f"{party_label}: {party_name}",
        f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        "-"*50,
        f"{'Product':15}{'Qty':>5}{'Free':>6}{'Rate':>10}{'Line Total':>15}",
        "-"*50,
    ]
    subtotal = 0.0
    for item in data['items']:
        name       = item['name']
        qty        = item['qty']
        free       = item.get('free', 0)
        rate       = item['unit_price']
        line_total = qty * rate
        subtotal  += line_total
        lines.append(f"{name:15}{qty:>5}{free:>6}{rate:>10.2f}{line_total:>15.2f}")

    vat   = subtotal * 0.13
    total = subtotal + vat
    lines += [
        "-"*50,
        f"{'Subtotal':>40} : Rs{subtotal:>8.2f}",
        f"{'VAT @13%':>40} : Rs{vat:>8.2f}",
        f"{'Total':>40} : Rs{total:>8.2f}",
        "="*50,
    ]
    invoice_text = "\n".join(lines)
    with open(fname, "w") as f:
        f.write(invoice_text)
    return invoice_text, fname
