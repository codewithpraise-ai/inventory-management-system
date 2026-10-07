import requests


BASE_URL = "https://world.openfoodfacts.org/api/v2"

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0"
}


def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/product/{barcode}.json"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "product_name": product.get("product_name", "Unknown"),
        "brands": product.get("brands", "Unknown"),
        "ingredients_text": product.get("ingredients_text", ""),
        "barcode": barcode
    }