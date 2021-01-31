from collections import OrderedDict
import nltk
import ssl
import pprint
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('vader_lexicon','nltk_data')
from .services import give_emoji_free_text, mytagme_ann, remove_urls, word_count, clean_text
from .serializers import TwitSerializer
from .models import Twit
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from decouple import config
import tweepy
import json 
import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from django.http import JsonResponse


auth = tweepy.OAuthHandler(config('ConsumerKey'), config('ConsumerSecret'))
auth.set_access_token(config('Key'), config('Secret'))
api = tweepy.API(auth)

class SearchResultView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = TwitSerializer

    def get(self,request ):
        key = request.query_params.get('key')
        tweet_count = request.query_params.get('tweetCount')
        tweets = tweepy.Cursor(api.search,
              tweet_mode='extended',
              q=key,
              lang='en').items(int(tweet_count))
        tweets_arr = []
        clean_tweet = ''
        clean_tweets = ''
        words = []
        json_str = '['
        full_text =''
        analyzer = SentimentIntensityAnalyzer()             
        for tweet in tweets:           
            full_text = tweet.full_text            
            hashtags = tweet.entities['hashtags']
            if hasattr(tweet, 'retweeted_status'):
                full_text = tweet.retweeted_status.full_text 
                hashtags = tweet.retweeted_status.entities['hashtags']
            json_str = json_str + json.dumps(tweet._json) + ','
            clean_tweet = give_emoji_free_text(full_text)
            clean_tweet = remove_urls(clean_tweet)             
            clean_tweets = clean_tweets + clean_text(clean_tweet)           
            tweets_arr.append({
                "text":full_text, 
                "sentiment":analyzer.polarity_scores(full_text), 
                "annotations": mytagme_ann(clean_tweet), 
                "hashtags": hashtags })
                

        words = word_count(clean_tweets)
        json_str = json_str[:-1]
        json_str = json_str + ']'
        result = {
            'search_key_word':key,
            'twits':json.loads(json_str),
            'cooked':tweets_arr,
            'created':datetime.datetime.now(),
            'clean_twits': clean_tweets,
            'user_id': str(request.user),
            'word_count': words
        }
        serializer = self.serializer_class(data=result)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'data': {
                    'twits': json.loads(json_str),
                    'cooked': tweets_arr,
                    'cleanTwits': clean_tweets,
                    'word_count': words
                } 
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

class HistoryListView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = TwitSerializer

    def get(self,request):
        data = Twit.objects.filter(user_id = request.user).values('id', 'created', 'search_key_word')
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'data':  data
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

import re
class HistoryView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = TwitSerializer

    def get(self, request, *args, **kwargs):
        item_id = int(kwargs.pop('id'))
        data = Twit.objects.filter(user_id = request.user, id = item_id )
        serializer = TwitSerializer(data, many=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'data':serializer.data[0]  
            }
        
        status_code = status.HTTP_200_OK

        return JsonResponse(response, status=status_code)

