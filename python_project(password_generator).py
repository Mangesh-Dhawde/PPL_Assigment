# 🔐 PASSWORD GENERATOR WEB APP USING FLASK

from flask import Flask, render_template_string, request
import random
import string

app = Flask(__name__)

# -------------------------------
# HTML TEMPLATE (inside Python)
# -------------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Generator</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(135deg, #667eea, #764ba2);
            text-align: center;
            padding: 50px;
            color: white;
        }
        .box {
            background: white;
            color: black;
            padding: 25px;
            border-radius: 10px;
            display: inline-block;
        }
        input, button {
            padding: 8px;
            margin: 5px;
        }
    </style>
</head>
<body>

<div class="box">
    <h2>🔐 Password Generator</h2>

    <form method="POST">
        Length: <input type="number" name="length" value="12"><br>

        <input type="checkbox" name="upper"> Uppercase<br>
        <input type="checkbox" name="lower"> Lowercase<br>
        <input type="checkbox" name="digits"> Numbers<br>
        <input type="checkbox" name="symbols"> Symbols<br><br>

        <button type="submit">Generate</button>
    </form>

    {% if password %}
        <h3>Password: {{password}}</h3>
        <h4>Strength: {{strength}}</h4>
    {% endif %}
</div>

</body>
</html>
"""

# -------------------------------
# Password Generator Logic
# -------------------------------
def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    pool = ""

    if use_upper:
        pool += string.ascii_uppercase
    if use_lower:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    if pool == "":
        return "Select at least one option!"

    password = ''.join(random.choice(pool) for _ in range(length))
    return password


# -------------------------------
# Strength Checker
# -------------------------------
def check_strength(password):
    strength = 0

    if any(c.islower() for c in password):
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1

    if len(password) >= 12:
        strength += 1

    if strength <= 2:
        return "Weak ❌"
    elif strength == 3:
        return "Medium ⚠️"
    else:
        return "Strong ✅"


# -------------------------------
# Main Route
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    password = None
    strength = None

    if request.method == "POST":
        length = int(request.form.get("length", 12))
        use_upper = "upper" in request.form
        use_lower = "lower" in request.form
        use_digits = "digits" in request.form
        use_symbols = "symbols" in request.form

        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)

        if "Select" not in password:
            strength = check_strength(password)

    return render_template_string(HTML_PAGE, password=password, strength=strength)


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)