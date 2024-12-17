import base64
import os
from flask import Blueprint, request, jsonify, send_from_directory
from config.db import db
from models.spectral_schema import validate_data

bp = Blueprint("spectral_routes", __name__, url_prefix="/spectral")

collection = db["Spectral_Values"]

# Directory to save images
IMAGE_FOLDER = "saved_images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def save_image_as_base64(file):
    """Encode image file as Base64."""
    try:
        return base64.b64encode(file.read()).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Error encoding image: {e}")

def save_base64_as_file(base64_string, filename):
    """Save Base64-encoded image as a file."""
    try:
        image_data = base64.b64decode(base64_string)
        file_path = os.path.join(IMAGE_FOLDER, filename)
        with open(file_path, "wb") as file:
            file.write(image_data)
        return file_path
    except Exception as e:
        raise ValueError(f"Error decoding and saving image: {e}")

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
    """Get all data and save images as files."""
    try:
        data = list(collection.find({}, {"_id": 0}))
        for item in data:
            if "image" in item and item["image"]:
                # Convert Base64 to file
                sample_id = item.get("Sample_Id", "unknown")
                filename = f"{sample_id}.jpg"
                file_path = save_base64_as_file(item["image"], filename)
                item["image_path"] = f"/spectral/images/{filename}"  # Add path to response
                del item["image"]  # Remove Base64 data to clean up response

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/data/<sample_id>", methods=["GET"])
def get_data_by_sample_id(sample_id):
    """Get data by Sample_Id and save image as file."""
    try:
        data = collection.find_one({"Sample_Id": sample_id}, {"_id": 0})
        if not data:
            return jsonify({"error": "Sample_Id not found"}), 404

        if "image" in data and data["image"]:
            filename = f"{sample_id}.jpg"
            file_path = save_base64_as_file(data["image"], filename)
            data["image_path"] = f"/spectral/images/{filename}"
            del data["image"]  # Remove Base64 data

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/images/<filename>", methods=["GET"])
def get_image(filename):
    """Serve the saved image file."""
    try:
        return send_from_directory(IMAGE_FOLDER, filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
