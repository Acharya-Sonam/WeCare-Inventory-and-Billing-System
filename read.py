def read_products():
    """
    Reads products.txt lines into list of dicts:
    name, brand, quantity (int), cost_price (float), country.
    """
    products = []
    with open("products.txt", "r") as f:
        for line in f:
            parts = line.strip().split(", ")
            if len(parts) != 5:
                continue
            name, brand, qty_s, cp_s, country = parts
            qty = int(qty_s)
            cp = float(cp_s)
            products.append({
                'name': name,
                'brand': brand,
                'quantity': qty,
                'cost_price': cp,
                'country': country
            })
    return products
