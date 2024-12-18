from flask import Flask, request, render_template
from markupsafe import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
        title="From sample",
        message="お名前は？")
    
@app.route('/', methods=['POST'])
def form():
    field=request.form['field']
    return render_template('idnex.html',
            title="Fron sample",
            message="こんにちは$s"%field)