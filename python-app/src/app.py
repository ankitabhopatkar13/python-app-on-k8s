import os
from flask import Flask, redirect

app = Flask(__name__)

APP_ENV = os.environ.get('APP_ENV')
DEBUG = APP_ENV == 'development'


def get_app_version():
    with open('VERSION.txt') as f:
        return f.read()


@app.route('/')
def home():
    return redirect('/version', code=302)


@app.route('/version')
def version():
    return get_app_version()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=DEBUG)
