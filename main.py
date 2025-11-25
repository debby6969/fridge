from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Store fridge items as a list of dicts
# Each entry looks like: {"name": "cheese", "expiry": date}
food = []

@app.route("/")
def index():
    today = datetime.date.today()
    events = [
        {"title": entry["name"], "start": entry["expiry"].strftime("%Y-%m-%d")}
        for entry in food
    ]
    return render_template("index.html", food=food, today=today, events=events)


@app.route("/add", methods=["POST"])
def add_item():
    itemname = request.form["itemname"].strip()
    expiry = request.form["expiry"].strip()

    if not itemname or not expiry:
        return "⚠️ Please provide both item name and expiry date in DD-MM-YYYY format. Make sure you add dashes(-) between numbers example : 12-12-2025.", 400

    try:
        expiry_date = datetime.datetime.strptime(expiry, "%d-%m-%Y").date()
    except ValueError:
        # Handle invalid date format
        return "❌ Invalid date format. Please use DD-MM-YYYY.", 400

    food.append({"name": itemname, "expiry": expiry_date})
    return redirect(url_for("index"))

    # Append new item to list (duplicates allowed)
    food.append({"name": itemname, "expiry": expiry_date})

    return redirect(url_for("index"))

@app.route("/remove", methods=["POST"])
def remove_item():
    itemname = request.form["itemname"]
    # Remove the first matching item (could extend to remove all)
    for entry in food:
        if entry["name"] == itemname:
            food.remove(entry)
            break
    return redirect(url_for("index"))

@app.route("/check")
def check_expiry():
    today = datetime.date.today()
    # Get 'days' from query string, default to 7 if not provided
    days = request.args.get("days", default=7, type=int)

    expired = []
    expiring_today = []
    soon3 = []
    soon = []

    for entry in food:
        expiry_date = entry["expiry"]
        if expiry_date < today:
            expired.append(entry["name"])
        elif expiry_date == today:
            expiring_today.append(entry["name"])
        elif today < expiry_date <= today + datetime.timedelta(days=days):
            soon.append(entry["name"])
            

    return render_template(
        "check.html",
        expired=expired,
        expiring_today=expiring_today,
        soon=soon,
        soon3=soon3,
        today=today,
        days=days
    )

@app.route("/secret")
def secret():
    return render_template("secret.html")
 
events = [
    {"title": entry["name"], "start": entry["expiry"].strftime("%Y-%m-%d")}
    for entry in food
]


if __name__ == "__main__":
    app.run(debug=True)
