#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script works with tweepy

# - tweepy installation/authentication tutorial:
# https://www.digitalocean.com/community/tutorials/how-to-authenticate-a-python-application-with-twitter-using-tweepy-on-ubuntu-14-04
# - tweepy tutorial:
# http://docs.tweepy.org/en/v3.5.0/getting_started.html#api
# - twitter and tweepy api reference:
# https://developer.twitter.com/en/docs/api-reference-index
# http://docs.tweepy.org/en/v3.5.0/api.html
# - number with commas as thousands separators:
# https://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators

try:
    import tweepy
    tweepyInstalled = 1
except:
    tweepyInstalled = 0

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

TWEETS = [
'https://twitter.com/StackOverflow/status/910133441286496256',
'https://twitter.com/github/status/913139368818331648',
'https://twitter.com/DisneySpain/status/915517354477592576'
]

# functions

def checksAndAlerts():
    if tweepyInstalled == 0:
        print 'Error. Install tweepy'
        return 0
    if CONSUMER_KEY == '' or CONSUMER_SECRET == '' or ACCESS_TOKEN == '' or ACCESS_TOKEN_SECRET == '':
        print 'Error. Not Twitter app credentials'
        return 0
    return 1

def getApi():
    AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(AUTH)
    return api

def getTweetValues(TWEET):
    TWEETID = int(TWEET.split('/')[-1])
    HANDLE = TWEET.split('/')[-3]
    return TWEETID, HANDLE

def getUserInfo(HANDLE):
    USEROBJECT = api.get_user(HANDLE)
    USER = USEROBJECT.name
    FOLLOWERS = "{:,}".format(USEROBJECT.followers_count).replace(',','.') # dots as thousands separators
    #HANDLE =  USEROBJECT.screen_name
    #CREATIONDATE = USEROBJECT.created_at
    return USER, FOLLOWERS

def getTweetInfo(TWEETID):
    TWEETINFO = api.get_status(TWEETID)
    RETWEETS = TWEETINFO.retweet_count
    LIKES = TWEETINFO.favorite_count
    return RETWEETS, LIKES

# main

if checksAndAlerts() == 1:
    api = getApi()
    for TWEET in TWEETS:
        TWEETID, HANDLE = getTweetValues(TWEET)
        USER, FOLLOWERS = getUserInfo(HANDLE)
        RETWEETS, LIKES = getTweetInfo(TWEETID)
        print 'Usuario: ' + USER + '. Handle: @' + HANDLE + '. Seguidores: ' + FOLLOWERS + u'. Retweets publicación: ' + str(RETWEETS) + u'. Likes publicación: ' + str(LIKES) + u'. Dirección publicación:'
        print TWEET
        print ''