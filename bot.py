# -*- coding: utf-8 -*-
import os
import message
from slackclient import SlackClient
import string
import datetime
import random

import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer

GLOBAL_COOLOFF_PERIOD = 5
SPECIFIC_COOLOFF_PERIOD = 5

stemmer = LancasterStemmer()
lemmatizer = WordNetLemmatizer()

authed_teams = {}

stop_words = set(stopwords.words('english'))

translator = str.maketrans('','',string.punctuation)

ad_categories = {
        'trip': 'hotel',
        'vac': 'hotel',
        'hotel': 'hotel',
        'book': 'book',
        'read': 'book',
        'movy': 'movie',
        'film': 'movie',
        'cinem': 'movie',
        'program': 'study',
        'study': 'study',
        'cod': 'study',
        'job': 'job',
        'interview': 'job',
        'tesl': 'car',
        'car': 'car',
        'automobl': 'car',
        'cryptocur': 'bitcoin',
        'ethere': 'bitcoin',
        'bitcoin': 'bitcoin',
        'blockchain': 'bitcoin',
        'chirstma': 'gift',
        'gift': 'gift',
        'watch': 'gift',
        'softw': 'azure',
	'cloud': 'azure'
        }
ad_words = set(ad_categories.keys())

last_ad_posted = [None]
ads = {
        'hotel': {'last_posted': None, 'ads': ['Check out great travel deals at TripAdvisor! https://www.tripadvisor.com/', 'Great offers await you at Expedia https://www.expedia.com/']},

        'book': {'last_posted': None, 'ads': ['Kindle eBooks, Kindle Holiday Deals, Save over 1000 great deals https://www.amazon.com/Kindle-eBooks/', 'This Holiday Season, Get all the books on your wish-list  https://www.barnesandnoble.com/']},

        'movie': {'last_posted': None, 'ads': ['Check out movies this week in AMC theatre near you https://www.amctheatres.com/', 'Catch your favourite movies in cinema near you on https://www.fandango.com/']},

        'study': {'last_posted': None, 'ads': ['Learn to code for free on https://www.codecademy.com/', 'You can learn anything.For free. For everyone. Forever. https://www.khanacademy.org/']},


        'job': {'last_posted': None, 'ads': ['Find a job that suits you at https://www.indeed.com/', 'Get updates on your job application every step of the way. https://www.ziprecruiter.com/']},

        'car': {'last_posted': None, 'ads': ['Quickest Acceleration.Longest Range. The Safest Cars Ever https://www.tesla.com/', ' Ultimate Price Transparency See what others paid before you buy or lease from TrueCar Certified Dealers  https://www.truecar.com/','Find all types of car here on your budget https://www.cars.com/']},

        'bitcoin': {'last_posted': None, 'ads': ['Buy Bitcoin Now Use your credit card to buy bitcoins, safely and quickly https://buy.bitcoin.com/', 'Buy and Sell digital currency https://www.coinbase.com/','Trade securely on the world most active digital asset exchange.https://poloniex.com/']},

        'gift': {'last_posted': None, 'ads': ['FIND THE PERFECT GIFT, EVERY TIME. https://www.gifts.com/', 'Find best gifts at https://www.amazon.com/gp/gift-finder']},

        'azure': {'last_posted': None, 'ads': ['Amazon Web Services offers reliable, scalable, and inexpensive cloud computing services https://aws.amazon.com/', 'Microsoft Azure is an open, flexible, enterprise-grade cloud computing platform https://azure.microsoft.com/']},


        }

class Bot(object):
    def __init__(self):
        super(Bot, self).__init__()
        self.name = "adservicesbot"
        self.emoji = ":robot_face:"
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot chat:write:bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")

        self.client = SlackClient("")
        self.messages = {}

    def auth(self, code):
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        self.client = SlackClient(authed_teams[team_id]["bot_token"])


    def send_reply(self, event, team_id, user_id):
        print('===')
        print(event)
        user_text = event['event']['text']

        #remove punctuation
        message = user_text.translate(translator)

        # tokenize
        tokens = nltk.word_tokenize(message)
        tokens = [t.lower() for t in tokens]

        # remove stopwords
        sanitized = filter(lambda x: x not in stop_words, tokens)

        # stemming
        stemmed = [stemmer.stem(t) for t in sanitized]

        # lemmatize
        lemmatized = {lemmatizer.lemmatize(t) for t in stemmed}

        # print extracted words
        print(user_text)
        print(lemmatized)
        target_ad_words = lemmatized.intersection(ad_words)

        if not target_ad_words: 
            return

        target_ad_word = list(target_ad_words)[0]
        target_category = ad_categories[target_ad_word]

        if last_ad_posted[0] and datetime.datetime.now() < (last_ad_posted[0] + datetime.timedelta(seconds=GLOBAL_COOLOFF_PERIOD)):
            return

        ad_record = ads[target_category]
        if ad_record['last_posted'] and datetime.datetime.now() < (ad_record['last_posted'] + datetime.timedelta(seconds=SPECIFIC_COOLOFF_PERIOD)):
            return
            
        ad_record['last_posted'] = datetime.datetime.now()
        last_ad_posted[0] = datetime.datetime.now()

        display_ad = random.choice(ad_record['ads'])
        post_message = self.client.api_call("chat.postMessage",
                                            channel=event['event']['channel'],
                                            text=display_ad,
                                            )
