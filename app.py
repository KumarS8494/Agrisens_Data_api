from flask import Flask
from routes import spectral_routes  
import os

app = Flask(__name__)

app.register_blueprint(spectral_routes.bp)

@app.route("/")
def home():
    return {"message": "Welcome to the Spectral Values API!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default to port 5000 if not provided
    app.run(host="0.0.0.0", port=port)
