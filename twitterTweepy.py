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
# - functions
# -- number with commas as thousands separators:
# https://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators
# -- delete list values
# https://stackoverflow.com/questions/2793324/is-there-a-simple-way-to-delete-a-list-element-by-value

try:
    import tweepy
    tweepyInstalled = 1
except:
    tweepyInstalled = 0

# values

languageSpanish = 's'
languageEnglish = 'e'
language = [languageSpanish] # select the desired language. Type list to allow selecting more than one

tweetsURLfile = 'tweetsURL.txt'

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# functions

def checksAndAlerts():
    if tweepyInstalled == 0:
        print 'Error. Install tweepy'
        return 0
    if CONSUMER_KEY == '' or CONSUMER_SECRET == '' or ACCESS_TOKEN == '' or ACCESS_TOKEN_SECRET == '':
        print 'Error. No Twitter app credentials'
        return 0
    if checkFileExists (tweetsURLfile) == 0:
        print 'Error. File "',tweetsURLfile,'" does not exist'
        return 0
    return 1

def getApi():
    AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(AUTH)
    return api

def checkFileExists(filePathAndName):
    try:
        open(filePathAndName,'r') # file name and extension
        return 1
    except:
        return 0

def getFileContentList (fileNameWithExtension):
    fileOpened = open(fileNameWithExtension)
    fileContent = fileOpened.read()
    fileOpened.close()
    fileContentList = fileContent.split('\n')
    fileContentList = [listValue for listValue in fileContentList if listValue != ''] # delete blank rows
    return fileContentList

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

def showResults(TWEETS, language):
    for TWEET in TWEETS:
        TWEETID, HANDLE = getTweetValues(TWEET)
        USER, FOLLOWERS = getUserInfo(HANDLE)
        RETWEETS, LIKES = getTweetInfo(TWEETID)
        if languageSpanish in language:
            print 'Usuario: ' + USER + '. Handle: @' + HANDLE + '. Seguidores: ' + FOLLOWERS + u'. Retweets publicación: ' + str(RETWEETS) + u'. Likes publicación: ' + str(LIKES) + u'. Dirección publicación:'
        if languageEnglish in language:
            print 'User: ' + USER + '. Handle: @' + HANDLE + '. Followers: ' + FOLLOWERS + '. Retweets: ' + str(RETWEETS) + '. Likes: ' + str(LIKES) + '. Post:'
        print TWEET
        print ''

# main

if checksAndAlerts() == 1:
    api = getApi()
    TWEETS = getFileContentList(tweetsURLfile)
    showResults(TWEETS, language)