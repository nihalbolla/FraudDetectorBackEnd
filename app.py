from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Import analyze function from your file
from FRAUD_monitor_final import analyze

app = Flask(__name__)
CORS(app)

# ---------------- HEALTH CHECK ----------------
@app.route("/")
def home():
    return jsonify({"message": "Fraud Detection API Running"}), 200

# ---------------- PREDICT ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Extract inputs
        amount = float(data.get("amount"))
        freq = int(data.get("freq"))
        hour = int(data.get("hour"))
        location = int(data.get("location"))

        # Call your main function
        score, decision, reasons, _ = analyze(amount, freq, hour, location)

        return jsonify({
            "risk_score": score,
            "decision": decision,
            "reasons": reasons
        }), 200

    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
