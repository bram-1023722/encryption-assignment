from flask import Flask, render_template, request, flash
import json
from crypto_utils import encrypt_with_password, decrypt_with_password

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-key"   # nodig voor flash-berichten

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    text = request.form.get("plaintext", "")
    password = request.form.get("password_enc", "")
    try:
        result = encrypt_with_password(text, password)
        json_result = json.dumps(result, indent=2, ensure_ascii=False)
        return render_template("index.html", enc_result=json_result)
    except Exception as e:
        flash(str(e))
        return render_template("index.html")

@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    package = request.form.get("package_json", "")
    password = request.form.get("password_dec", "")
    try:
        plaintext = decrypt_with_password(package, password)
        return render_template("index.html", dec_result=plaintext)
    except Exception as e:
        flash(str(e))
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
