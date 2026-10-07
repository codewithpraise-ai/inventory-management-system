from unittest.mock import patch

from app import cli


@patch("app.cli.requests.get")
def test_view_inventory(mock_get, capsys):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "product_name": "Milk",
            "brands": "Test Brand",
            "price": 100,
            "stock": 10
        }
    ]

    cli.view_inventory()

    output = capsys.readouterr().out

    assert "Milk" in output
    assert "Test Brand" in output


@patch("app.cli.requests.post")
@patch("builtins.input")
def test_add_item(mock_input, mock_post):
    mock_input.side_effect = [
        "Bread",
        "Test Bread",
        "150",
        "20",
        "789012"
    ]

    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "id": 2,
        "product_name": "Bread"
    }

    cli.add_item()

    mock_post.assert_called_once()


@patch("app.cli.requests.patch")
@patch("builtins.input")
def test_update_item(mock_input, mock_patch):
    mock_input.side_effect = [
        "1",
        "120",
        "15"
    ]

    mock_patch.return_value.json.return_value = {
        "id": 1,
        "price": 120,
        "stock": 15
    }

    cli.update_item()

    mock_patch.assert_called_once()


@patch("app.cli.requests.delete")
@patch("builtins.input")
def test_delete_item(mock_input, mock_delete):
    mock_input.return_value = "1"

    mock_delete.return_value.json.return_value = {
        "message": "Inventory item deleted successfully"
    }

    cli.delete_item()

    mock_delete.assert_called_once()


@patch("app.cli.requests.get")
@patch("builtins.input")
def test_find_product(mock_input, mock_get):
    mock_input.return_value = "737628064502"

    mock_get.return_value.json.return_value = {
        "product_name": "Thai peanut noodle kit"
    }

    cli.find_product()

    mock_get.assert_called_once()