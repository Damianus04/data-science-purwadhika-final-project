# standard flask libraries
from os import name, sep
from flask import Flask, render_template, request
import pandas as pd
import json
import time
from datetime import datetime
from joblib import load
import joblib
from sklearn.externals import joblib
import nltk

# my functions
from static.src.helpers import get_tweets, predict_sentiment
from static.src.helpers import text_preprocessing

# data
real_estate = pd.read_csv('./data/melb_data.csv')
model = load('model/rand_search_logreg_hyper_tfidf.joblib')

app = Flask(__name__)


# text_sample_prediction = model.predict(text_sample)
# print(model_joblib)
# print(text_sample_prediction)

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

            # Preprocessing 'tweet_text'
            tweet_data['tweet_text_preprocessed'] = tweet_data['tweet_text'].apply(
                lambda x: text_preprocessing(x)
            )

            # Predict Twitter Text
            prediction_list = predict_sentiment(
                model, tweet_data, colname='tweet_text_preprocessed')
            tweet_data['sentiment'] = prediction_list

            # DEFINE ONLY BAD SENTIMENT
            # tweet_data = tweet_data[tweet_data['sentiment'] == -1]

            sentiment_chart = tweet_data[['sentiment', 'tweet_text']].groupby(
                ['sentiment'], as_index=False).count()
            tweet_sentiment_label = list(sentiment_chart.sentiment)
            tweet_sentiment_values = list(sentiment_chart.tweet_text)

            # potential reach data
            reach_data = tweet_data[['screen_name', 'followers']].head(
                10).sort_values(by='followers', ascending=False)
            reach_data_screen_name = list(reach_data.screen_name)
            reach_data_followers = list(reach_data.followers)

            # word distribution
            word_freq_dist_dict = []
            for i in tweet_data.tweet_text_preprocessed:
                word_freq_dist_dict.extend(i.split(' '))

            word_freq_dist = nltk.FreqDist(word_freq_dist_dict)
            top10words = word_freq_dist
            top10words = word_freq_dist.most_common(20)
            words = []
            words_frequency = []
            for i in top10words:
                words.append(i[0])
                words_frequency.append(i[1])

            # location distribution
            top10locations = pd.DataFrame(
                tweet_data['location'].value_counts())[:20]
            locations = top10locations.index
            locations_frequency = [i for i in top10locations.location]

        except:
            tweet_legend = "conversations"
            tweet_time_label = ['None']
            tweet_count_values = [0]
            tweet_sentiment_label = ['None']
            tweet_sentiment_values = [0]
            reach_data_screen_name = ['None']
            reach_data_followers = [0]
            words = ['None']
            words_frequency = [0]
            locations = ['None']
            locations_frequency = [0]

    # Melbourne Data
    df_Regionname = df[['Price', 'Regionname']].groupby(
        ['Regionname'], as_index=False).mean()
    legend = 'Average Price'
    labels = list(df_Regionname.Regionname)
    values = list(df_Regionname.Price)

    return render_template('index.html',
                           data=df, tweet_data=tweet_data, text_query=text_query,
                           total_mentions=total_mentions, average_mentions=average_mentions,
                           legend=legend, labels=labels, values=values,
                           tweet_time_label=tweet_time_label, tweet_count_values=tweet_count_values, tweet_legend=tweet_legend,
                           tweet_sentiment_label=tweet_sentiment_label, tweet_sentiment_values=tweet_sentiment_values,
                           reach_data_screen_name=reach_data_screen_name, reach_data_followers=reach_data_followers,
                           words=words, words_frequency=words_frequency, locations=locations, locations_frequency=locations_frequency
                           )


@app.route('/bad-sentiment', methods=["GET", "POST"])
def bad_sentiment():
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

            # DEFINE ONLY BAD SENTIMENT
            # tweet_data = tweet_data[tweet_data['sentiment'] == -1]

            # Preprocessing 'tweet_text'
            tweet_data['tweet_text_preprocessed'] = tweet_data['tweet_text'].apply(
                lambda x: text_preprocessing(x)
            )

            # Predict Twitter Text
            prediction_list = predict_sentiment(
                model, tweet_data, colname='tweet_text_preprocessed')
            tweet_data['sentiment'] = prediction_list

            sentiment_chart = tweet_data[['sentiment', 'tweet_text']].groupby(
                ['sentiment'], as_index=False).count()
            tweet_sentiment_label = list(sentiment_chart.sentiment)
            tweet_sentiment_values = list(sentiment_chart.tweet_text)

            # potential reach data
            reach_data = tweet_data[['screen_name', 'followers']].head(
                10).sort_values(by='followers', ascending=False)
            reach_data_screen_name = list(reach_data.screen_name)
            reach_data_followers = list(reach_data.followers)

            # word distribution
            word_freq_dist_dict = []
            for i in tweet_data.tweet_text_preprocessed:
                word_freq_dist_dict.extend(i.split(' '))

            word_freq_dist = nltk.FreqDist(word_freq_dist_dict)
            top10words = word_freq_dist
            top10words = word_freq_dist.most_common(20)
            words = []
            words_frequency = []
            for i in top10words:
                words.append(i[0])
                words_frequency.append(i[1])

            # location distribution
            top10locations = pd.DataFrame(
                tweet_data['location'].value_counts())[:20]
            locations = top10locations.index
            locations_frequency = [i for i in top10locations.location]

        except:
            tweet_legend = "conversations"
            tweet_time_label = ['None']
            tweet_count_values = [0]
            tweet_sentiment_label = ['None']
            tweet_sentiment_values = [0]
            reach_data_screen_name = ['None']
            reach_data_followers = [0]
            words = ['None']
            words_frequency = [0]
            locations = ['None']
            locations_frequency = [0]

    # Melbourne Data
    df_Regionname = df[['Price', 'Regionname']].groupby(
        ['Regionname'], as_index=False).mean()
    legend = 'Average Price'
    labels = list(df_Regionname.Regionname)
    values = list(df_Regionname.Price)

    return render_template('bad-sentiment.html',
                           tweet_data=tweet_data, text_query=text_query,
                           total_mentions=total_mentions, average_mentions=average_mentions,
                           legend=legend, labels=labels, values=values,
                           tweet_time_label=tweet_time_label, tweet_count_values=tweet_count_values, tweet_legend=tweet_legend,
                           tweet_sentiment_label=tweet_sentiment_label, tweet_sentiment_values=tweet_sentiment_values,
                           reach_data_screen_name=reach_data_screen_name, reach_data_followers=reach_data_followers,
                           words=words, words_frequency=words_frequency, locations=locations, locations_frequency=locations_frequency
                           )


if __name__ == '__main__':
    app.run(debug=True)
