from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Zcash Insight is running!"

if __name__ == "__main__":
    app.run(debug=True)