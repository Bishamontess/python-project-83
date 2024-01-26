from flask import Flask

app = Flask(__name__)


@app.route('/')
def main():
    return "<p>Welcome to webpage's analyzer!</p>"
