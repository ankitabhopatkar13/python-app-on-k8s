from flask import Flask
app = Flask(__name__)


def get_app_version():
    with open('VERSION.txt') as f:
        return f.read()


@app.route('/version')
def version():
    return get_app_version()


if __name__ == '__main__':
    app.run()
