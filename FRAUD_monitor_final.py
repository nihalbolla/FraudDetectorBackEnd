import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# -------- DARK THEME --------
plt.style.use("dark_background")

print("SMART FRAUD DETECTION SYSTEM (FINAL)")
print("=" * 60)

# ---------------- TRAIN DATA ----------------
X = np.array([
    [100,1,10,0],
    [500,2,12,0],
    [1000,3,14,0],
    [3000,2,15,0],
    [5000,5,16,0],
    [10000,4,18,0],
    [20000,3,12,0],
    [50000,2,14,0],
])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_scaled)

history_scores = []
history_labels = []

plt.ion()

# ---------------- ANALYSIS ----------------
def analyze(amount, freq, hour, location):
    reasons = []
    contributions = {}
    risk_score = 0

    # -------- SAFE ZONE (KEY FIX) --------
    if amount <= 10000 and freq <= 5 and location == 0 and 6 <= hour <= 22:
        return 10, "ALLOW", ["Normal transaction behavior"], {"Safe": 100}

    test = scaler.transform([[amount, freq, hour, location]])
    pred = model.predict(test)[0]
    ml_score = (1 - model.decision_function(test)[0]) * 100

    # -------- RULES --------
    if amount > 20000 and freq > 10:
        risk_score += 25
        reasons.append("High amount + frequency")
        contributions["Amount"] = 25

    if freq > 10:
        risk_score += 20
        reasons.append("High frequency")
        contributions["Frequency"] = 20

    if hour < 5:
        risk_score += 15
        reasons.append("Night transaction")
        contributions["Night"] = 15

    if location != 0:
        risk_score += 20
        reasons.append("International transaction")
        contributions["Location"] = 20

    # -------- REDUCED ML IMPACT --------
    if pred == -1:
        risk_score += 10
        reasons.append("ML anomaly (low confidence)")
        contributions["ML"] = 10

    # -------- SMART RELAXATION --------
    if amount > 30000 and freq <= 3 and location == 0:
        risk_score -= 25
        reasons.append("Trusted high-value behavior")
        contributions["Trusted"] = -25

    # -------- FINAL SCORE --------
    final_score = min(100, max(0, round((ml_score * 0.3 + risk_score * 0.7), 2)))

    decision = "BLOCK" if final_score > 65 else "ALLOW"

    return final_score, decision, reasons, contributions

# ---------------- DASHBOARD ----------------
def update_dashboard():
    plt.clf()

    # -------- TOP: TREND --------
    plt.subplot(3,1,1)
    plt.plot(history_scores, marker='o', linewidth=2)
    plt.title("Live Risk Score Trend")
    plt.ylabel("Risk %")
    plt.grid(alpha=0.3)

    # -------- MIDDLE: BAR --------
    plt.subplot(3,1,2)
    if history_scores:
        latest = history_scores[-1]
        plt.bar(["Current Risk"], [latest])
        plt.ylim(0,100)
        plt.title(f"Current Risk Score: {latest}%")

    # -------- BOTTOM: PIE --------
    plt.subplot(3,1,3)
    safe = history_labels.count("ALLOW")
    fraud = history_labels.count("BLOCK")

    if safe + fraud > 0:
        plt.pie(
            [safe, fraud],
            labels=["Safe", "Fraud"],
            autopct='%1.1f%%',
            startangle=90
        )

    plt.title("Transaction Distribution")

    plt.tight_layout()
    plt.pause(0.5)

# ---------------- MAIN LOOP ----------------
if __name__ == "__main__":
    while True:
        print("\nNew Transaction")
        print("-" * 40)

        try:
            amount = float(input("Amount (₹): "))
            freq = int(input("Transactions/hour: "))
            hour = int(input("Hour (0-23): "))
            loc = input("Location (IN/OUT): ").upper()

            location = 0 if loc == "IN" else 1

            score, decision, reasons, contributions = analyze(amount, freq, hour, location)

            history_scores.append(score)
            history_labels.append(decision)

            print("\nRESULT")
            print("-" * 40)
            print(f"Risk Score : {score}%")

            if decision == "BLOCK":
                print("FRAUD DETECTED")
            else:
                print("SAFE TRANSACTION")

            print("\nReasons:")
            for r in reasons:
                print("-", r)

        # -------- CONTRIBUTION PIE --------
            if contributions:
                labels = list(contributions.keys())
                sizes = [abs(v) for v in contributions.values()]

                plt.figure()
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                plt.title("Fraud Contribution Breakdown")
                plt.show()

        # -------- UPDATE DASHBOARD --------
            update_dashboard()

        except:
            print("Invalid input")
