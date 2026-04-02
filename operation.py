from read import read_products
from write import write_products, generate_invoice

def is_valid_name(name: str) -> bool:
    """
    Returns True if `name` is non-empty and contains only letters and spaces.
    """
    name = name.strip()
    if not name:
        return False
    for c in name:
        if not (c.isalpha() or c == ' '):
            return False
    return True

def sales_operation():
    """
    1) Display all products with selling price (2×cost_price) and stock
    2) Process customer sale with Buy 3 Get 1 Free
    3) Deduct stock, save back to products.txt
    4) Generate and display a sales invoice including 13% VAT
    """
    try:
        products = read_products()
    except:
        print("\nCannot load products.\n")
        return

    if not products:
        print("\nNo products available.\n")
        return

    print("\n--- Available Products for Sale ---")
    for p in products:
        sp = p['cost_price'] * 2
        print(f"{p['name']} ({p['brand']}) – Rs{sp:.2f}, Qty: {p['quantity']}")
    print()

    # Get and validate customer name
    raw_customer = input("Enter customer name: ")
    if not is_valid_name(raw_customer):
        print("Error: Name must contain only letters and spaces.")
        return
    customer = raw_customer.strip()

    data = {'customer_name': customer, 'items': []}

    while True:
        raw_name = input("\nEnter product name (or 'done'): ")
        name = raw_name.strip().lower()
        if name == 'done':
            break

        found = False
        for p in products:
            if p['name'].strip().lower() == name:
                found = True
                try:
                    qty = int(input("Enter quantity: ").strip())
                    if qty <= 0:
                        print("Quantity must be > 0.")
                        break
                except ValueError:
                    print("Invalid quantity.")
                    break

                free = qty // 3
                needed = qty + free
                if p['quantity'] < needed:
                    print(f"Insufficient stock ({p['quantity']} available).")
                    break

                p['quantity'] -= needed
                sp = p['cost_price'] * 2
                data['items'].append({
                    'name': p['name'],
                    'brand': p['brand'],
                    'qty': qty,
                    'free': free,
                    'unit_price': sp
                })
                print(f"Added {qty} (+{free} free).")
                break

        if not found:
            print("Product not found.")

    if not data['items']:
        print("\nNo items sold.\n")
        return

    write_products(products)
    invoice_text, filename = generate_invoice(data, "sale")
    print("\n" + invoice_text)
    print(f"Invoice saved as: {filename}\n")


def restock_operation():
    """
    1) Display all products with current cost price and stock
    2) Process vendor restock entries (including adding new products)
    3) Update inventory, save back to products.txt
    4) Generate and display a restock invoice including 13% VAT
    """
    try:
        products = read_products()
    except Exception as e:
        print(f"\nCannot load products: {e}\n")
        return

    if not products:
        print("\nNo products loaded.\n")
        return

    # Display current inventory
    print("\n--- Current Inventory for Restock ---")
    for p in products:
        print(f"{p['name']} ({p['brand']}) – Cost Price: Rs{p['cost_price']:.2f}, Stock: {p['quantity']}")
    print()

    # Get and validate vendor name
    raw_vendor = input("Enter vendor name: ").strip()
    if not is_valid_name(raw_vendor):
        print("Error: Name must contain only letters and spaces.")
        return
    vendor = raw_vendor

    data = {'vendor_name': vendor, 'items': []}

    while True:
        raw_name = input("\nEnter product to restock (or 'done'): ").strip()
        if raw_name.lower() == 'done':
            break

        # Look up existing product
        key = raw_name.lower()
        existing = next((p for p in products if p['name'].strip().lower() == key), None)

        if existing:
            # Restock existing product
            try:
                qty = int(input(f"Enter quantity to add for '{existing['name']}': ").strip())
                price = float(input("Enter updated cost price: ").strip())
                if qty <= 0 or price < 0:
                    print("Quantity must be > 0 and price >= 0.")
                    continue
            except ValueError:
                print("Invalid input. Please enter valid numbers for quantity and price.")
                continue

            existing['quantity'] += qty
            existing['cost_price'] = price
            data['items'].append({
                'name': existing['name'],
                'brand': existing['brand'],
                'qty': qty,
                'unit_price': price
            })
            print(f"Restocked {qty} units of '{existing['name']}'.")

        else:
            # Optionally add a new product
            resp = input(f"Product '{raw_name}' not found. Add as new product? (y/n): ").strip().lower()
            if resp not in ('y', 'yes'):
                continue

            new_name = raw_name
            brand = input("Enter brand: ").strip()
            if not brand:
                print("Error: Brand cannot be empty.")
                continue
            try:
                qty = int(input("Enter initial stock quantity: ").strip())
                price = float(input("Enter cost price: ").strip())
                if qty < 0 or price < 0:
                    print("Quantity and price must be non-negative.")
                    continue
            except ValueError:
                print("Invalid input. Please enter valid numbers for quantity and price.")
                continue

            new_prod = {
                'name': new_name,
                'brand': brand,
                'quantity': qty,
                'cost_price': price
            }
            products.append(new_prod)
            data['items'].append({
                'name': new_name,
                'brand': brand,
                'qty': qty,
                'unit_price': price
            })
            print(f"Added new product '{new_name}' with {qty} units.")

    if not data['items']:
        print("\nNo items were restocked.\n")
        return

    # Save updated inventory
    try:
        write_products(products)
        print("\nInventory updated successfully.")
    except Exception as e:
        print(f"Error saving inventory: {e}")
        return

    # Generate and display restock invoice
    try:
        invoice_text, filename = generate_invoice(data, "restock")
        print("\n" + invoice_text)
        print(f"Invoice saved as: {filename}\n")
    except Exception as e:
        print(f"Error generating invoice: {e}")
