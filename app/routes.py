from flask import Blueprint, jsonify, request

from app.inventory import inventory, get_next_id
from app.external_api import get_product_by_barcode

inventory_bp = Blueprint("inventory", __name__)


# GET all inventory
@inventory_bp.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


# GET one inventory item
@inventory_bp.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    return jsonify(item), 200


# POST a new inventory item
@inventory_bp.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "product_name",
        "brands",
        "price",
        "stock",
        "barcode"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    if not isinstance(data["price"], (int, float)) or data["price"] < 0:
        return jsonify({
            "error": "Price must be a non-negative number"
        }), 400

    if not isinstance(data["stock"], int) or data["stock"] < 0:
        return jsonify({
            "error": "Stock must be a non-negative integer"
        }), 400

    new_item = {
        "id": get_next_id(),
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data.get("ingredients_text", ""),
        "price": data["price"],
        "stock": data["stock"],
        "barcode": data["barcode"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


# PATCH an inventory item
@inventory_bp.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "price" in data:
        if not isinstance(data["price"], (int, float)) or data["price"] < 0:
            return jsonify({"error": "Invalid price"}), 400

        item["price"] = data["price"]

    if "stock" in data:
        if not isinstance(data["stock"], int) or data["stock"] < 0:
            return jsonify({"error": "Invalid stock"}), 400

        item["stock"] = data["stock"]

    if "product_name" in data:
        item["product_name"] = data["product_name"]

    if "brands" in data:
        item["brands"] = data["brands"]

    return jsonify(item), 200


# DELETE an inventory item
@inventory_bp.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = next(
        (item for item in inventory if item["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    inventory.remove(item)

    return jsonify({
        "message": "Inventory item deleted successfully"
    }), 200

@inventory_bp.route("/products/barcode/<barcode>", methods=["GET"])
def find_product(barcode):
    try:
        product = get_product_by_barcode(barcode)

        if product is None:
            return jsonify({
                "error": "Product not found"
            }), 404

        return jsonify(product), 200

    except Exception:
        return jsonify({
            "error": "External API request failed"
        }), 502


@inventory_bp.route("/inventory/from-api/<barcode>", methods=["POST"])
def add_from_api(barcode):
    try:
        product = get_product_by_barcode(barcode)

        if product is None:
            return jsonify({
                "error": "Product not found"
            }), 404

        new_item = {
            "id": get_next_id(),
            "product_name": product["product_name"],
            "brands": product["brands"],
            "price": 0,
            "stock": 0,
            "barcode": product["barcode"],
            "ingredients_text": product["ingredients_text"]
        }

        inventory.append(new_item)

        return jsonify(new_item), 201

    except Exception:
        return jsonify({
            "error": "External API request failed"
        }), 502