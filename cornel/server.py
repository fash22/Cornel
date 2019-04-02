from flask import Flask, render_template, url_for, redirect, abort

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))