

from operation import sales_operation, restock_operation
from read import read_products

def display_menu():
    while True:
        print("\n--- Welcome to WeCare Store ---\n")
        print("1. Display the products")
        print("2. Sales")
        print("3. Restock")
        print("4. Exit\n")

        choice = input("Enter choice: ").strip()
        if choice == '1':
            try:
                prods = read_products()
                print("\n--- Products (Buy 3 Get 1 Free) ---\n")
                for p in prods:
                    sp = p['cost_price'] * 2  # selling price
                    print(f"{p['name']} ({p['brand']}) - Rs{sp:.2f}, Qty: {p['quantity']}")
                print()
            except Exception:
                print("\nCannot display products.\n")

        elif choice == '2':
            sales_operation()

        elif choice == '3':
            restock_operation()

        elif choice == '4':
            print("\nGoodbye!\n")
            break

        else:
            print("\nInvalid choice. Please enter 1-4.\n")

if __name__ == "__main__":
    display_menu()
