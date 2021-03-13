# standard flask libraries
from os import name, sep
from flask import Flask, render_template, request
import pandas as pd
import json

# visualization library
import plotly
import plotly.graph_objs as go

# my functions
from static.src.plot import get_tweets

# text = get_tweets('vaksin')
# print(text)

# data
# df = pd.read_csv("./data/final_text_data.csv")
real_estate = pd.read_csv('./data/melb_data.csv')
# print(real_estate.head())
# print(df.head())


app = Flask(__name__)


# ROUTE FUNCTION
# route to index.html
@app.route('/')
def index():
    # Dummy Melbourne Data
    table = real_estate.head(100)
    return render_template('index.html', data=table)


@app.route('/', methods=["GET", "POST"])
def keyword_search():
    # Dummy Melbourne Data
    table = real_estate.head(100)

    # Get Tweet
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        # Get Tweet
        text_query = request.form['text']
        tweet_data = get_tweets(text_query)
        total_mentions = len(tweet_data)
        average_mentions = round(total_mentions/7)

    return render_template('index.html',
                           data=table, tweet_data=tweet_data, text_query=text_query,
                           total_mentions=total_mentions, average_mentions=average_mentions
                           )


if __name__ == '__main__':
    app.run(debug=True)
