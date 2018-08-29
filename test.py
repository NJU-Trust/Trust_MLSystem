from flask import Flask
from flask_cors import *
from credit_rating import load

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    return "hello"


@app.route("/credit_rating", methods=["GET", "POST"])
def credit_rating():
    return load.predict()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)