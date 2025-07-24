from flask import Flask, render_template, Response
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/firebase-config.js")
def firebase_config_js():
    config = f"""
    const firebaseConfig = {{
        apiKey: "{os.getenv("FIREBASE_API_KEY")}",
        authDomain: "{os.getenv("FIREBASE_AUTH_DOMAIN")}",
        projectId: "{os.getenv("FIREBASE_PROJECT_ID")}",
        storageBucket: "{os.getenv("FIREBASE_STORAGE_BUCKET")}",
        messagingSenderId: "{os.getenv("FIREBASE_MESSAGING_SENDER_ID")}",
        appId: "{os.getenv("FIREBASE_APP_ID")}",
        measurementId: "{os.getenv("FIREBASE_MEASUREMENT_ID")}"
    }};
    firebase.initializeApp(firebaseConfig);
    """
    return Response(config, mimetype='application/javascript')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
