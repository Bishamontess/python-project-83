from flask import Flask, render_template
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    return render_template(
        'layout.html',
    )
