import tweepy
import credentials as cred
import pymongo
import json
import logging



import requests



API_KEY = cred.API_KEY
API_SECRET = cred.API_SECRET
ACCESS_TOKEN = cred.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = cred.ACCESS_TOKEN_SECRET

# Create listeer
# create stream object
# start the stream
my_auth = tweepy.OAuthHandler(API_KEY, API_SECRET)

# Listen to specific key words from stream
class Listener(tweepy.StreamListener):
    
    def on_data(self, raw_data):
        data = self.process_data(raw_data)
        data = json.loads(data)
        fill_mongo_db(data)
 
        # Return true to keep connection open
        return True

    def process_data(self, raw_data):
        #print(raw_data)
        return raw_data

    # close the stream when an error occurs
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

    def get_data(self):
        return self.data
    
    
# Create the streamer that will listen to the twitter API
class Stream():
    # The first function that is called when this class is initialized
    def __init__(self,auth,listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    # Define how to start the stream
    def start(self, keywords):
        self.stream.filter(track=keywords)

#client = MongoClient('example.com',
#                      username='user',
#                      password='password',
#                      authSource='the_database',
#                      authMechanism='SCRAM-SHA-256')

# when running locally then use ==> host='0.0.0.0', port=27019 / container ==> host="mongo_db", port=27017
def fill_mongo_db(tweet_data_raw):
    client = pymongo.MongoClient(host="mongo_db", port=27017)
    # create a database called twitter_db 
    # twitter_db will be called db in our script
    db = client.twitter_db
    post = tweet_data_raw

    # create a collection
    tweet_collection = db.tweet_data
    #tweet_id = tweet_collection.insert_one(post)
    tweet_collection.insert_one(post)

    print(post)
    logging.critical("Inserting into mongoDB"+str(post))
    # Check what tweets were inserted into the collection
    #for doc in tweet_collection.find():
    #    print(doc)
      

# search for keywords

def keyword_search():
    input_keywords = input("Enter keywords to search for: ")
    return input_keywords

# Start everthing by coding the main method
if __name__ == '__main__':
    #keyword = keyword_search()
    
    # Set the default keyword to none
    # if 'none' then the streamer will not be initialized
    keyword='none'
    try:
        keyword = keyword_search()
    except Exception as e:
        logging.critical('No Input')
    # Create the listener
    listener = Listener()
    
    # Create an authentication object
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    # Set the access token and access token secret
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    
    # Inintialize Stream object with the listener and auth
    # Then start the stream
    start_stream = Stream(auth, listener)
    #logging.critical("ran once")
    if keyword=='none':
        logging.critical("No Keyword")
    else:
        start_stream.start(['#'+str(keyword)])