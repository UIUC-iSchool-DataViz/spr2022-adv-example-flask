import matplotlib.pyplot as plt
import io
import numpy as np
import pandas as pd
from flask import Flask, send_file, render_template, jsonify, Response
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, {}! It\'s me, your new server.'

@app.route('/plot/<int:count>/', defaults = {'marker_type': 'o'})
@app.route('/plot/<int:count>/marker_type/<marker_type>')
def make_plot(count, marker_type):
    x = np.random.random(count)
    y = np.random.random(count)
    plt.clf()
    plt.scatter(x, y, marker=marker_type)
    b = io.BytesIO()
    plt.savefig(b, format='png')
    b.seek(0)
    return send_file(b, 'image/png')

@app.route('/random-data/', defaults = {'count': 100})
@app.route('/random-data/<int:count>')
def random_data(count):
    return Response(pd.DataFrame({'data': np.random.random(count)}).to_json(orient='records'), mimetype='application/json')

@app.route('/hello/<string:name>')
def hello(name):
    return render_template('index.html', name = name)

@app.route('/example-json/')
def example_json():
    return jsonify({'a': [1, 2], 'b': {'c': 6, 'd': "something"}})

@app.route('/gallery/', defaults = {'count': 10})
@app.route('/gallery/<int:count>')
def gallery(count):
    return render_template('gallery.html', count = count, name = "Gallery")
