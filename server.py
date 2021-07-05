from flask import Flask, jsonify, render_template, request, session, Response, send_from_directory, redirect
import json
from busqueda import buscar

app = Flask(__name__, template_folder= "")
app._static_folder = "web/static"

@app.route('/')
def index():
    return render_template("web/static/html/index.html")

@app.route('/buscarServer', methods=['POST'])
def buscarServer():
    if (not request.is_json):
        c = json.loads(request.data)['values']
    else:
        c = json.loads(request.data)
    return Response(json.dumps(buscar(c['query'], 3)), status = 201, mimetype = "application/json")

if __name__ == '__main__':
    app.run(port=8080, threaded=True, host=('127.0.0.1'))