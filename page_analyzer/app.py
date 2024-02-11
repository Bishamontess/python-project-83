from flask import (Flask, render_template, redirect, flash, url_for, request)
import psycopg2
from psycopg2.extras import NamedTupleCursor
from urllib.parse import urlparse
import validators
from dotenv import load_dotenv
from datetime import datetime
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
load_dotenv(override=True)
DATABASE_URL = os.getenv('DATABASE_URL')
try:
    connect = psycopg2.connect(DATABASE_URL)
except:
    print('Can`t establish connection to database')


@app.route('/')
def index():
    return render_template('index.html',)


@app.route('/urls/', methods=['GET', 'POST'])
def urls_table():
    if request.method == 'POST':
        url_for_search = request.form['url']
        url_id = get_normalized_url(url_for_search)
        # url_for('urls_id', id=url_id)
        return make_flash(url_for_search)
    return render_template('index.html',)


@app.route('/urls/<int:url_id>')
def urls_id(url_for_search):
    url_info = get_url_info(url_for_search)
    return render_template(
        'url_id.html',
        url_id=url_info.url_id,
        url_name=url_info.url_name,
        created_at=url_info.created_at,
    )


def is_url_in_db(url_for_search):
    with connect.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE name=%s',
                     get_normalized_url(url_for_search))
        url_info = curs.fetchall()
        return url_info.url_name


def add_url_in_db(url_for_search):
    with connect.cursor() as curs:
        curs.execute('INSERT INTO urls (name, created_at) VALUES (%s,%s)',
                     (get_normalized_url(url_for_search),
                      datetime.now().date()))
    connect.close()


def get_url_info(url_for_search):
    return is_url_in_db(url_for_search)


def get_normalized_url(url_for_search):
    parsed_url = urlparse(url_for_search)
    return parsed_url[0] + '://' + parsed_url[1]


def is_url_valid(url_for_search):
    return validators.url(url_for_search) and len(url_for_search) <= 255


def make_flash(url_for_search):
    if is_url_valid(url_for_search):
        if is_url_in_db(url_for_search) is None:
            add_url_in_db(url_for_search)
            flash('')
            return render_template('/flashes/url_added.html')
        else:
            flash('')
            return render_template('/flashes/url_exists.html')
    else:
        if url_for_search:
            flash('')
            return render_template('/flashes/url_wrong.html')
        else:
            flash('')
            return render_template('/flashes/url_is_required.html')
