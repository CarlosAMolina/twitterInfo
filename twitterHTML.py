#!/usr/bin/env python
# _*_ coding: utf-8

# This script works with tweets' HTML
# https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
# https://stackoverflow.com/questions/12572362/get-a-string-after-a-specific-substring

import re
import urllib

# values

tweetsURLfile = 'tweetsURL.txt'

NOVALUE = 'N/A'

# terms to find desired values
WEB2 = '/status'
USER1 = ['" data-name="']
USER2 = ['" data-protected="']
HANDLE1 = ['data-screen-name="', 'twitter.com/']
HANDLE2 = ['" data-name="', '/status/']
FOLLOW1 = ['" title="']
FOLLOW2 = ['" data-nav="followers"']
LIKE1 = ['Megusta"><strong>']
LIKE2 = ['</strong>Megusta']
RETWEET1 = ['retweets"><strong>']
RETWEET2 = ['</strong>Retweets']

# functions

def checksAndAlerts():
    if checkFileExists (tweetsURLfile) == 0:
        print 'Error. File "',tweetsURLfile,'" does not exist'
        return 0
    return 1

def getValueBetween (whereFind, search1, search2):
    if len(search1)==len(search2):
        i=0
        VALUE = NOVALUE
        while VALUE == NOVALUE and i < len(search1):
            VALUE = re.search(search1[i]+'(.*)'+search2[i], whereFind)
            if VALUE != None: # result
                VALUE = VALUE.group(1)
            else:
                VALUE=NOVALUE
            if len(VALUE) > 40: # bad search
                VALUE=NOVALUE
            i += 1
        return VALUE
    else:
        return NOVALUE

def getValueBefore (whereFind, search):
    VALUE = whereFind.split(search,1)[0]
    return VALUE

def getHTML(url):
    f = urllib.urlopen(url)
    HTML = f.read()
    return HTML

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

def saveFile (fileName, value):
    file = open (fileName, 'w')
    try:
        file.write (value)
    except:
        value = value.encode('utf-8')
        file.write (value)
    file.close()

def readFile (fileName):
    f = open (fileName, 'r')
    value = f.read()
    f.close()
    return value

# main

if checksAndAlerts() == 1:

    TWEETS = getFileContentList(tweetsURLfile)
    for TWEET in TWEETS:
        WEB = getValueBefore (TWEET, WEB2)
        WEBHTML = getHTML (WEB)
        TWEETHTML = getHTML (TWEET)
    
        WEBHTML = WEBHTML.decode ('utf-8')
        TWEETHTML = TWEETHTML.replace (" ", "")
        TWEETHTML = "".join(TWEETHTML.splitlines())
    
        USER = getValueBetween (WEBHTML, USER1, USER2)
        HANDLE = getValueBetween (WEBHTML, HANDLE1, HANDLE2)
        FOLLOWERS = getValueBetween (WEBHTML, FOLLOW1, FOLLOW2).split()[0]
        LIKES = getValueBetween (TWEETHTML, LIKE1, LIKE2)
        RETWEET = getValueBetween (TWEETHTML, RETWEET1, RETWEET2)
    
        print 'Usuario: ' + USER + '. Handle: @' + HANDLE + '. Seguidores: ' + FOLLOWERS + u'. Retweets publicación: ' + RETWEET + u'. Likes publicación: ' + LIKES + u'. Dirección publicación:'
        print TWEET
        print ''