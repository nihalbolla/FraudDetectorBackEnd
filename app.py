from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

model = pickle.load(open("FRAUD_monitor_final.py", "rb"))

@app.route("/")
def home():
    return "ML API Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["features"]
    prediction = model.predict([data])
    return jsonify({"prediction": prediction.tolist()})

if __name__ == "__main__":
    app.run()
