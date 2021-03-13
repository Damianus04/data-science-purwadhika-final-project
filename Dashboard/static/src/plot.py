import pandas as pd
import tweepy
import time
pd.set_option('display.max_colwidth', 1000)

# api key
api_key = "VF9Xv4WxUBUBMrH2yntvW2DD0"
# api secret key
api_secret_key = "mzZU8SQUXHwYThBO0mtk3hkQG9JYhZ6byJoIjlwcBTagSG4Nkn"
# access token
access_token = "473787030-HUT2iebZltM6XjswhV7fnGpQerksZ5a7qaoyEJjp"
# access token secret
access_token_secret = "LkvliySmLd57Wt8LVVpy1nJ5jlRwaQo1wzfyh0epYzJ8d"

authentication = tweepy.OAuthHandler(api_key, api_secret_key)
authentication.set_access_token(access_token, access_token_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True)


def get_profile_banner_url(i):
    if 'profile_banner_url' in i.user._json:
        return i.user.profile_banner_url
    else:
        return 'None'


def get_news_url_2(i):
    if i.entities['urls'] == []:
        return 'None'
    else:
        return i.entities['urls'][0]['url']


def get_tweets(keyword='indonesia', location="-0.789275,113.921326,5000km", language='id'):
    # list to store tweets
    tweets_list = []
    # no of tweets
    count = 100
    # location
    location = location
    # lang
    language = language
    try:
        # Pulling individual tweets from query
        for tweet in api.search(q=keyword, geocode=location, count=count, lang=language):
            # print(tweet.text)
            # Adding to list that contains all tweets
            tweets_list.append({'tweet_id': tweet.id,
                                'user_name': tweet.user.name,
                                'screen_name': tweet.user.screen_name,
                                'profile_url': f"https://twitter.com/{tweet.user.screen_name}",
                                'created_at': tweet.created_at,
                                'tweet_text': tweet.text,
                                'location': tweet.user.location,
                                'followers': tweet.user.followers_count,
                                'following': tweet.user.friends_count,
                                'listed_count': tweet.user.listed_count,
                                'profile_image': tweet.user.profile_image_url,
                                'profile_banner_image': get_profile_banner_url(tweet),
                                'news_url_1': tweet.user.url,
                                'news_url_2': get_news_url_2(tweet)})
        # return tweets_list
        return pd.DataFrame.from_dict(tweets_list)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)


# def get_tweets(text_query):
#     # list to store tweets
#     tweets_list = []
#     # no of tweets
#     count = 50
#     try:
#         # Pulling individual tweets from query
#         for tweet in api.search(q=text_query, count=count):
#             # print(tweet.text)
#             # Adding to list that contains all tweets
#             tweets_list.append({'created_at': tweet.created_at,
#                                 'tweet_id': tweet.id,
#                                 'tweet_text': tweet.text})
#         # return tweets_list
#         return pd.DataFrame.from_dict(tweets_list)

#     except BaseException as e:
#         print('failed on_status,', str(e))
#         time.sleep(3)
