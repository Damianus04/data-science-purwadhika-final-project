# standard flask libraries
from os import name, sep
from flask import Flask, render_template, request
import pandas as pd
import json

# visualization library
import plotly
import plotly.graph_objs as go

# data
df = pd.read_csv("data/final_text_data.csv")

app = Flask(__name__)


# ROUTE FUNCTION
# route to index.html
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
