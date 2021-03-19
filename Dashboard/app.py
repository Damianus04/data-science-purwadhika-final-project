# standard flask libraries
from os import name, sep
from flask import Flask, render_template, request
import pandas as pd
import json
import time
from datetime import datetime

# my functions
from static.src.helpers import get_tweets

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

        # add text tweet stats
        total_mentions = len(tweet_data)
        if total_mentions == 0 or text_query == " ":
            average_mentions = 0
        else:
            average_mentions = round(total_mentions/7)

        try:
            # add detailed datetime features
            tweet_data['date'] = tweet_data.created_at.apply(
                lambda x: x.date())
            tweet_data['day'] = tweet_data.created_at.apply(
                lambda x: x.day_name())
            tweet_data['month'] = tweet_data.created_at.apply(
                lambda x: x.month_name())
            tweet_data['year'] = tweet_data.created_at.apply(
                lambda x: x.year)
            tweet_data['time1'] = tweet_data.created_at.apply(
                lambda x: x.to_period('H').strftime('%d-%b-%y'))
            tweet_data['time2'] = tweet_data.created_at.apply(
                lambda x: x.to_period('H').strftime('%d-%b-%y %H:%M'))

            time1 = tweet_data[['time1', 'tweet_text']].groupby(
                ['time1'], as_index=False).count()
            time2 = tweet_data[['time2', 'tweet_text']].groupby(
                ['time2'], as_index=False).count()

            tweet_legend = "conversations"
            # choose whether to use time1 (day & hour) or time2 (hour)
            if len(time1.time1) > 1:
                tweet_time_label = list(time1.time1)
                tweet_count_values = list(time1.tweet_text)
            else:
                tweet_time_label = list(time2.time2)
                tweet_count_values = list(time2.tweet_text)
        except:
            tweet_legend = "conversations"
            tweet_time_label = ['None']
            tweet_count_values = [0]

    # Chart.js
    df_Regionname = df[['Price', 'Regionname']].groupby(
        ['Regionname'], as_index=False).mean()
    legend = 'Average Price'
    labels = list(df_Regionname.Regionname)
    values = list(df_Regionname.Price)

    return render_template('index.html',
                           data=df, tweet_data=tweet_data, text_query=text_query,
                           total_mentions=total_mentions, average_mentions=average_mentions,
                           legend=legend, labels=labels, values=values,
                           tweet_time_label=tweet_time_label, tweet_count_values=tweet_count_values, tweet_legend=tweet_legend
                           )


if __name__ == '__main__':
    app.run(debug=True)
