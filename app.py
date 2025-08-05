from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data = pd.read_csv("results.csv")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_result', methods=["POST"])
def get_result():
    req = request.get_json()
    roll = req["rollNumber"].strip().lower()
    branch = req["branch"].strip().lower()
    semester = req["semester"].strip().lower()

    match = data[
        (data["roll"].str.lower() == roll) &
        (data["branch"].str.lower() == branch) &
        (data["semester"].astype(str).str.lower() == semester)
    ]

    if not match.empty:
        result = match.iloc[0]
        session['result'] = {
            "Name": str(result["name"]),
            "Roll": str(result["roll"]),
            "Branch": str(result["branch"]),
            "Semester": str(result["semester"]),
            "CGPA": float(result["cgpa"])  # convert to float to ensure JSON serializability
        }
        return {"status": "redirect", "url": "/result"}
    else:
        return {"status": "not_found"}

@app.route('/result')
def result():
    if 'result' in session:
        return render_template("result.html", result=session['result'])
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
