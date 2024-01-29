from flask import Flask, render_template,redirect, get_flashed_messages, url_for
from urllib.parse import urlparse
from dotenv import load_dotenv
from validators.url import url
import os


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def main():
    return render_template(
        'layout.html',
    )


@app.route('/urls')
def urls_table():
    return render_template(
        'urls.html'
    )


@app.route('/urls/<int>:id')
def urls_id(url_id):
    return render_template(
        'url_id.html',
        url=url_id,
    )


@app.post('/')
def make_flash():
    flash('Страница успешно добавлена') #зеленый текст на салатовом
    flash('Страница уже существует')  #синий текст на голубом
    flash('Некорректный URL') #красный текст на розовом
    flash('Произошла ошибка при проверке') #красный текст на розовом
    return redirect(url_for('main'))


@app.get('/')
def flash():
    messages = get_flashed_messages(with_categories=True)
    print(messages)
    return render_template(
        'flash.html',
        messages=messages,
    )
