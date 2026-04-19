from flask import Flask, render_template
from routes import key_bp, encrypt_bp, decrypt_bp, test_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(key_bp)
app.register_blueprint(encrypt_bp)
app.register_blueprint(decrypt_bp)
app.register_blueprint(test_bp)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tests")
def tests_page():
    return render_template("tests.html")

if __name__ == "__main__":
    app.run(debug=True)
    