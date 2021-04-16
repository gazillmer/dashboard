import pandas as pd
import tweepy
import nltk
import numpy as np
import re
import unicodedata
import preprocessor as p
import plotly.graph_objects as go
import pathlib

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app

from datetime import datetime

CHARSET = 'UTF-8'

# Get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
DESTINATIONS_LIST = DATA_PATH.joinpath('destinations_list.csv')
AIRPORTS_LIST = DATA_PATH.joinpath('airport_list.csv')

# Get keys for authentication
apiKey = 'R3yUgmFxfpN7WM1tau2OX4ugi'
apiKeySecret = 'zS3vo85J5e8mK3Bw6O9NQ0abudGsIugn4VwVHgTYdSqVSZr4JB'
accessToken = '34781588-xvshSLi1vQsT3nrOFjIQDUEp2fHWBK7tx6RWsGJz1'
accessTokenSecret = 'DQg39vFtc9XXqiCDP4m1nZEXkp6h7yLvyBLiXUAk9bD0I'
mapbox_access_token = 'pk.eyJ1IjoiZ2F6aWxsbWVyIiwiYSI6ImNrbHdyNTM1azBsejUyc214aTMxbGxtbXEifQ.zHhMMVkUWYvLsOOC2MsmdA'

destinations = pd.read_csv(DESTINATIONS_LIST, encoding = CHARSET)

'''
# Create the authentication object
auth = tweepy.AppAuthHandler(apiKey, apiKeySecret)
api  = tweepy.API(auth)

# Search tweets about a destination and return a dataframe with the data
def get_destination_intentions(destination):
    
    # Initialize tweet fields as blank dictionaries
    tweet_dest, tweet_id, tweet_user, tweet_ot, tweet_source, tweet_date, tweet_location = ([] for i in range(7))
    
    # Describe possible travel intentions and search tweets about each one of them  
    intentions_list = ['viajar', 'visitar', 'conhecer']
    
    for intention in intentions_list:
        keyword = str(intention + ' ' + destination)
        tweets_json = api.search(q = keyword, count = 1000, lang='pt')
        
        # Append each tweet_field into the right tweet_field list
        for tweet in range(len(tweets_json)):
            tweet_dest.append(destination) 
            tweet_id.append(tweets_json[tweet].id)
            tweet_user.append(tweets_json[tweet].user.screen_name)
            tweet_ot.append(tweets_json[tweet].text)
            tweet_source.append(tweets_json[tweet].source)
            tweet_date.append(tweets_json[tweet].created_at)
            tweet_location.append(tweets_json[tweet].user.location)
    
    # Transforms all tweet_field lists into a dataframe and return it
    d = {'destination':tweet_dest,
         'id' : tweet_id,
         'user':tweet_user, 
         'date':tweet_date, 
         'original_text':tweet_ot, 
         'source':tweet_source, 
         'location' : tweet_location}
    
    # If tweepy_json returns any result for a given destination, print the number of results
    if(len(tweets_json) > 0):
        print(str(len(tweets_json)) + ' tweets about ' + destination)
    else:
        print('no tweets about ' + destination)
        
    return pd.DataFrame(data = d)



for index, dest in destinations['destination'].iteritems():
    if index == 0:
        tweets = get_destination_intentions(dest)
    else:
        tweets = tweets.append(get_destination_intentions(dest), ignore_index=True)

# Replace line break for a space
tweets['text'] = tweets['original_text'].astype('str') 
tweets['text'] = tweets['text'].str.replace('R$', '')
tweets['text'] = tweets['text'].str.replace('\n', ' ')

# Remove accents in tweet
def remove_accents(text):
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

tweets['text'] = tweets['text'].apply(remove_accents)

# Clean tweet, removing quotes, retweet marks and hashtags
for index in tweets.index:
    tweets.loc[index, 'text'] = p.clean(tweets.loc[index, 'text'])
tweets.head()

tweets['text'] = tweets['text'].str.lower()


tweets['text'] = tweets['text'].apply(remove_punctuation)

# Transform text into tokens for better processing
tweets['tokens'] = tweets.apply(lambda row: nltk.word_tokenize(row['text']), axis=1)

# Append user to tokens
for index in tweets.index:
    tweets.loc[index, 'tokens'].append(tweets.loc[index, 'user'])

tweets.drop_duplicates(subset='text', inplace=True)
'''

tweets = pd.read_csv('C:/Users/Zillmer/Google Drive/TCC/dashboard-heroku/datasets/tweets.csv', encoding = CHARSET)

tweets_per_dest = tweets.groupby('destination').count()
tweets_per_dest = tweets_per_dest.reset_index()[['destination', 'id']]

airports = pd.read_csv('C:/Users/Zillmer/Google Drive/TCC/dashboard-heroku/datasets/airport_list.csv', encoding = CHARSET)

tweets_per_dest = pd.merge(destinations, tweets_per_dest)
tweets_per_dest.rename(columns={'id' : 'tweets'}, inplace=True)
tweets_per_dest.drop(columns=['continent', 'country', 'destination'], inplace=True)
tweets_per_dest = tweets_per_dest.groupby('airport_iata').sum('tweets')
tweets_per_dest.reset_index(inplace=True)

tweets_per_airport = pd.merge(tweets_per_dest, airports[['airport_iata', 'lat', 'lon', 'name']])
tweets_per_airport.sort_values('tweets', ascending=False, inplace=True)

def plot_tweets():
    fig = go.Figure(go.Scattermapbox(
                lat=tweets_per_airport['lat'],
                lon=tweets_per_airport['lon'],
                mode='markers',
                text = tweets_per_airport['name'],
                marker=go.scattermapbox.Marker(
                    size=tweets_per_airport['tweets'] / 5,
                )
            )    
        )

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style = 'outdoors',
            bearing=2,
            center=go.layout.mapbox.Center(
                lat=-13,
                lon=-53
            ),
            pitch=0,
            zoom=3
        ),
        height = 600
    )
    return fig

map_tweets = plot_tweets()

layout = html.Div([
    html.H1('Travel mentions on Twitter', style={"textAlign": "center"}),
    dcc.Graph(id='my-tweets', figure=map_tweets)
])


