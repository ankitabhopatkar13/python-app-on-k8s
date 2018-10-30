from flask import Flask
app = Flask(__name__)

# TODO: Read from version file
VERSION = '1.0.0'


@app.route('/version')
def version():
    return VERSION


if __name__ == '__main__':
    app.run()
