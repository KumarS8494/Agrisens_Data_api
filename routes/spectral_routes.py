import base64
from flask import Blueprint, request, jsonify
from config.db import db
from models.spectral_schema import validate_data

bp = Blueprint("spectral_routes", __name__, url_prefix="/spectral")

collection = db["Spectral_Values"]

def save_image_as_base64(file):
    try:
        return base64.b64encode(file.read()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Error encoding image: {e}")

@bp.route("/add", methods=["POST"])
def add_data():
    """Add a new Spectral_Values document with optional image upload."""
    try:
        data = request.form.to_dict()  
        is_valid, error = validate_data(data)
        if not is_valid:
            return jsonify({"error": error}), 400

        if "image" in request.files:
            image_file = request.files["image"]
            data["image"] = save_image_as_base64(image_file) 

        result = collection.insert_one(data)
        return jsonify({"message": "Data added successfully!", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/data", methods=["GET"])
def get_all_data():
    try:
        data = list(collection.find({}, {"_id": 0}))  
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/data/<sample_id>", methods=["GET"])
def get_data_by_sample_id(sample_id):
    try:
        data = collection.find_one({"Sample_Id": sample_id}, {"_id": 0})
        if not data:
            return jsonify({"error": "Sample_Id not found"}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
