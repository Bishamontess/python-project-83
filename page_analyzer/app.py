from flask import Flask
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    return "<p>Welcome to webpage's analyzer!</p>"
