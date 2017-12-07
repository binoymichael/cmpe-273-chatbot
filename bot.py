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
SPECIFIC_COOLOFF_PERIOD = 30

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

#travel
hotel1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Deals at TripAdvisor!",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Check out great travel deals at TripAdvisor!",
    "text": " https://www.tripadvisor.com/",
    "thumb_url": "https://static.tacdn.com/img2/branding/trip_logo_footer@2x.png	"
}]

hotel2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Expedia deals for you",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Great offers await you at Expedia",
    "text": "https://www.expedia.com/",
    "thumb_url": "http://photos.prnewswire.com/prn/20110121/SF33870LOGO-b"
}]
#book

book1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Amazon Deals for Book-Lover",
    "color": "#9C1A22",
    "pretext": "Kindle eBooks, Kindle Holiday Deals, Save over 1000 great deals",
    "mrkdwn_in": ["text","fields"],
    "text": " https://www.amazon.com/Kindle-eBooks/",
    "thumb_url": "https://images-na.ssl-images-amazon.com/images/G/01/kindle/dp/2016/KP/feature-exclusives._CB301410435_.jpg"
}]

book2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Barnes and Noble holiday offers",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "This Holiday Season, Get all the books on your wish-list",
    "text": "https://www.barnesandnoble.com/",
    "thumb_url": "https://d2fv3018rxy7bx.cloudfront.net/website/wp-content/uploads/2015/11/barnes1.png"
}]

#movie
movie1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "AMC Theatre ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Check out movies this week in AMC theatre near you",
    "text": "https://www.amctheatres.com/",
    "thumb_url": "https://vignette.wikia.nocookie.net/logopedia/images/5/5b/Amc.jpg/revision/latest?cb=20120503012834"
}]


movie2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Fandango deals ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Catch your favourite movies in cinema near you ",
    "text": " https://www.fandango.com/",
    "thumb_url": "https://images.fandango.com/r1.0.50/redesign/static/img/fandango-logo.svg"
}]


#study
study1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Programming at codeacademy ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Learn to code for free on  ",
    "text": " https://www.codecademy.com/",
    "thumb_url": "http://sm.pcmag.com/t/pcmag_uk/review/c/codecademy/codecademy_24qd.640.jpg"
}]

study2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Khanacademy study for free ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "You can learn anything.For free. For everyone. Forever.  ",
    "text": "https://www.khanacademy.org/",
    "thumb_url": "https://vignette.wikia.nocookie.net/khanacademy/images/0/09/Khan-logo-vertical-transparent.png/revision/latest?cb=20150525225518"
}]

#jobs
jobs1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Your dream job at Indeed ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Find a job that suits you at   ",
    "text": "https://www.indeed.com/",
    "thumb_url": "https://tctechcrunch2011.files.wordpress.com/2012/09/job_search_indeed_en_gb.png"
}]

jobs2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Zip recruiter jobs for you ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Get updates on your job application every step of the way. ",
    "text": "https://www.ziprecruiter.com/ ",
    "thumb_url": "https://prnewswire2-a.akamaihd.net/p/1893751/sp/189375100/thumbnail/entry_id/1_ql9r3pcx/def_height/800/def_width/800/version/100011/type/2/q/100"
}]

#car
car1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Tesla electric cars ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Quickest Acceleration.Longest Range. The Safest Cars Ever   ",
    "text": "https://www.tesla.com/",
    "thumb_url": "http://www.carlogos.org/logo/Tesla-logo-2003-2500x2500.png"
}]

car2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Fair Price at True cars ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": " Ultimate Price Transparency See what others paid before you buy or lease from TrueCar Certified Dealers  ",
    "text": " https://www.truecar.com/",
    "thumb_url": "https://a.tcimg.net/pac/b/b72b3d71c2f832fc3941febfedd1d56f19455bff.png"
}]

car3 = [{
    "fallback": "The attachement isn't supported.",
    "title": "cars.com Holiday deals ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Find all types of car here on your budget  ",
    "text": "https://www.cars.com/",
    "thumb_url": "https://www.cars.com/static/www/logo-cars.png"
}]

#bitcoin
bitcoin1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Get bitcoin with you credit card ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Buy Bitcoin Now Use your credit card to buy bitcoins, safely and quickly  ",
    "text": "https://buy.bitcoin.com/",
    "thumb_url": "https://www.bitcoin.com/wp-content/uploads/2017/09/bitcoin-com-logo2.jpeg"
}]

bitcoin2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Get bitocin at coinbase ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Buy and Sell digital currency   ",
    "text": "https://www.coinbase.com/",
    "thumb_url": "https://s3.amazonaws.com/bittrust/coinbase_logo_white.png"
}]

bicoin3 = [{
    "fallback": "The attachement isn't supported.",
    "title": "poloneix bitcoin exchanage ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Trade securely on the world most active digital asset exchange.   ",
    "text": "https://poloniex.com/",
    "thumb_url": "https://steemit-production-imageproxy-upload.s3.amazonaws.com/DQmc9ffrdA4JZVYqho915NjEX5YZSoDG2zn1pBWgSQzMDrV"
}]


#gift
gift1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Amazon gifts for adults ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Find best gifts only on Amazon   ",
    "text": "https://www.amazon.com/gp/gift-finder",
    "thumb_url": "http://media.corporate-ir.net/media_files/IROL/17/176060/img/logos/amazon_logo_RGB.jpg"
}]

gift2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Holiday gifts on gifts.com ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "FIND THE PERFECT GIFT, EVERY TIME. FOR EVERYONE ",
    "text": "https://www.gifts.com/",
    "thumb_url": "https://pbs.twimg.com/profile_images/548591600377421825/QKtMa3cz.jpeg"
}]

#azure


azure1 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Amazon Web Services ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Amazon Web Services offers reliable, scalable, and inexpensive cloud computing services  ",
    "text": "https://aws.amazon.com/",
    "thumb_url": "https://a0.awsstatic.com/main/images/logos/aws_logo_smile_1200x630.png"
}]

azure2 = [{
    "fallback": "The attachement isn't supported.",
    "title": "Microsoft Azure ",
    "color": "#9C1A22",
    "mrkdwn_in": ["text","fields"],
    "pretext": "Microsoft Azure is an open, flexible, enterprise-grade cloud computing platform  ",
    "text": "https://azure.microsoft.com/",
    "thumb_url": "https://media.licdn.com/mpr/mpr/AAEAAQAAAAAAAAllAAAAJDJiNWQyOGNmLTJlYmYtNDUzMC04OTM5LWIyMmRkMTQyMDMwMg.png"
}]


ads = {
        'hotel': {'last_posted': None, 'ads': [hotel1, hotel2]},
        'book': {'last_posted': None, 'ads': [book1, book2]},
        'movie': {'last_posted': None, 'ads': [movie1, movie2]},
        'study': {'last_posted': None, 'ads': [study1, study2]},
        'job': {'last_posted': None, 'ads': [jobs1, jobs2]},
        'car': {'last_posted': None, 'ads': [car1, car2, car3]},
        'bitcoin': {'last_posted': None, 'ads': [bitcoin1, bitcoin2]},
        'gift': {'last_posted': None, 'ads': [gift1, gift2]},
        'azure': {'last_posted': None, 'ads': [azure1, azure2]},
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
                                            attachments=display_ad,
                                            )
