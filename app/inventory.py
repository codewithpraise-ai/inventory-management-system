inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 450.00,
        "stock": 20,
        "barcode": "1234567890123"
    },
    {
        "id": 2,
        "product_name": "Corn Flakes",
        "brands": "Kellogg's",
        "ingredients_text": "Corn, sugar, malt flavor",
        "price": 350.00,
        "stock": 15,
        "barcode": "2345678901234"
    }
]


def get_next_id():
    if not inventory:
        return 1

    return max(item["id"] for item in inventory) + 1