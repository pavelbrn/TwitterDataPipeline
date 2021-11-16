import tweepy
import credentials as cred

API_KEY = cred.API_KEY
API_SECRET = cred.API_SECRET
ACCESS_TOKEN = cred.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = cred.ACCESS_TOKEN_SECRET

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

# Start everthing by coding the main method
if __name__ == '__main__':
    # Create an authentication object
    auth2 = tweepy.OAuthHandler(API_KEY, API_SECRET)
    # Set the access token and access token secret
    auth2.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = auth2, listener=myStreamListener)
    myStream.filter(track=['python'])