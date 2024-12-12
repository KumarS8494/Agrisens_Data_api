from flask import Flask
from routes import spectral_routes  

app = Flask(__name__)

app.register_blueprint(spectral_routes.bp)

@app.route("/")
def home():
    return {"message": "Welcome to the Spectral Values API!"}

if __name__ == "__main__":
    app.run(debug=True)
