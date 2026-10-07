import requests


BASE_URL = "http://127.0.0.1:5000"


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("Inventory is empty.")
            return

        for item in items:
            print(
                f"ID: {item['id']} | "
                f"Product: {item['product_name']} | "
                f"Brand: {item['brands']} | "
                f"Price: {item['price']} | "
                f"Stock: {item['stock']}"
            )
    else:
        print("Failed to retrieve inventory.")


def add_item():
    product_name = input("Product name: ")
    brands = input("Brand: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    barcode = input("Barcode: ")

    data = {
        "product_name": product_name,
        "brands": brands,
        "price": price,
        "stock": stock,
        "barcode": barcode
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )

    if response.status_code == 201:
        print("Item added successfully.")
        print(response.json())
    else:
        print("Failed to add item.")
        print(response.json())


def update_item():
    item_id = int(input("Enter item ID: "))

    price = input("New price (leave blank to keep current): ")
    stock = input("New stock (leave blank to keep current): ")

    data = {}

    if price:
        data["price"] = float(price)

    if stock:
        data["stock"] = int(stock)

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    print(response.json())


def delete_item():
    item_id = int(input("Enter item ID: "))

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    print(response.json())


def find_product():
    barcode = input("Enter barcode: ")

    response = requests.get(
        f"{BASE_URL}/products/barcode/{barcode}"
    )

    print(response.json())


def add_from_api():
    barcode = input("Enter barcode: ")

    response = requests.post(
        f"{BASE_URL}/inventory/from-api/{barcode}"
    )

    print(response.json())


def main():
    while True:
        print("\n=== INVENTORY MANAGEMENT SYSTEM ===")
        print("1. View inventory")
        print("2. Add inventory item")
        print("3. Update inventory item")
        print("4. Delete inventory item")
        print("5. Find product on OpenFoodFacts")
        print("6. Add product from OpenFoodFacts")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            find_product()
        elif choice == "6":
            add_from_api()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()