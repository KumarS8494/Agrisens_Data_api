REQUIRED_FIELDS = [
    "410", "450", "470", "490", "510", "530", "550", "570", "590", "610",
    "630", "650", "670", "690", "710", "730", "860", "940", "Sample_Id",
    "Timestamp","lattitude", "longitude", "weather", "city","Species"
]

def validate_data(data):
    missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"
    return True, None
