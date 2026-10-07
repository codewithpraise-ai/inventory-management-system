from unittest.mock import patch

from app.external_api import get_product_by_barcode


@patch("app.external_api.requests.get")
def test_get_product_by_barcode(mock_get):
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Water, almonds"
        }
    }

    mock_get.return_value.raise_for_status.return_value = None

    result = get_product_by_barcode("123456789")

    assert result["product_name"] == "Organic Almond Milk"
    assert result["brands"] == "Silk"
    assert result["barcode"] == "123456789"


@patch("app.external_api.requests.get")
def test_product_not_found(mock_get):
    mock_get.return_value.json.return_value = {
        "status": 0
    }

    mock_get.return_value.raise_for_status.return_value = None

    result = get_product_by_barcode("000000000")

    assert result is None