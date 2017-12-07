#!/usr/bin/env python
# _*_ coding: utf-8

# This script works with tweets' HTML

import re
import urllib

# tweets to study
TWEETS = [
'https://twitter.com/StackOverflow/status/910133441286496256',
'https://twitter.com/github/status/913139368818331648',
'https://twitter.com/DisneySpain/status/915517354477592576'
]

# functions

NOVALUE = 'N/A'

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

# main
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


# https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
# https://stackoverflow.com/questions/12572362/get-a-string-after-a-specific-substring