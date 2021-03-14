# standard flask libraries
from os import name, sep
from flask import Flask, render_template, request
import pandas as pd
import json

# my functions
from static.src.helpers import get_tweets
from static.src.helpers import box_plot

# visualization
# import plotly.graph_objs as go
# import plotly

# text = get_tweets('vaksin')
# print(text)

# data
real_estate = pd.read_csv('./data/melb_data.csv')


app = Flask(__name__)


########## ROUTE FUNCTION ##########
# Route to index.html
@app.route('/')
def index():
    # Dummy Melbourne Data
    table = real_estate.head(100)
    return render_template('index.html', data=table)


@app.route('/', methods=["GET", "POST"])
def keyword_search():
    # Dummy Melbourne Data
    df = real_estate

    # Get Tweet
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        # Get Tweet
        text_query = request.form['text']
        tweet_data = get_tweets(text_query)
        total_mentions = len(tweet_data)
        if total_mentions == 0 or text_query == " ":
            average_mentions = 0
        else:
            average_mentions = round(total_mentions/7)

    # Chart.js
    df_Regionname = df[['Price', 'Regionname']].groupby(
        ['Regionname'], as_index=False).mean()
    legend = 'Average Price'
    labels = list(df_Regionname.Regionname)
    values = list(df_Regionname.Price)

    return render_template('index.html',
                           data=df, tweet_data=tweet_data, text_query=text_query,
                           total_mentions=total_mentions, average_mentions=average_mentions,
                           legend=legend, labels=labels, values=values
                           )

# Route to boxplot.html
@app.route('/box-plot')
def boxplot_route():
    table = real_estate.head(100)
    x_axis = 'Distance'
    list_x = [('Distance', 'Distance')]

    # Running scatter_plot function
    bar = box_plot(real_estate, x_axis)

    # return all variables
    return render_template('boxplot.html', plot=bar, data=table, focus_x=x_axis, drop_x=list_x)


if __name__ == '__main__':
    app.run(debug=True)
