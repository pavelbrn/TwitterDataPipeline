import logging
import pymongo
import time
import sqlalchemy
import pyjokes
import requests
import sqlalchemy as dbase
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Establish a connection to the MongoDB server
# When running locally then use ==> host='0.0.0.0', port=27019 / container ==> host="mongo_db", port=27017
client = pymongo.MongoClient(host="mongo_db", port=27017)

# Select the database you want to use withing the MongoDB server
# Has to be the same db name as in the MongoDB server thats running
db = client.twitter_db
docs = db.tweet_data.find()

# Let mongoBD have some time to start up
time.sleep(10)

# This collection mae be the same as the one in the MongoDB server!

# when running locally then use ==> 0.0.0.0:5555/postgreCOMP  inside container==> postgresdb:5432
pg = sqlalchemy.create_engine('postgresql://pavel:123@postgresdb:5432/postgreCOMP', echo=False)

pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment VARCHAR(500)
);
''')

# Run the sentiment analyzer on each tweet
analyzer = SentimentIntensityAnalyzer()
def sentiment_analysis(text):
    vs = analyzer.polarity_scores(text)
    compound_score = "{}".format(str(vs))
    logging.critical(compound_score)

    return compound_score


def post_to_postgre():
    for doc in docs:
        text = doc['text']
        score = sentiment_analysis(text)
        query = "INSERT INTO tweets VALUES (%s, %s);"
        pg.execute(query, (text, score))


# The following section posts our tweets to our specific Slack channel

webhook_url = "https://hooks.slack.com/services/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"

# when running locally then use ==> 0.0.0.0:5555/postgreCOMP  inside container==> postgresdb:5432
engine = dbase.create_engine('postgresql://pavel:123@postgresdb:5432/postgreCOMP', echo=False)

connection = engine.connect()
metadata = dbase.MetaData()
tweets = dbase.Table('tweets', metadata, autoload=True, autoload_with=engine)

query = dbase.select([tweets])
result_pr = connection.execute(query)
result_set = result_pr.fetchall()
a = result_set[:10]

webhook_url = "https://hooks.slack.com/services/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"


# Post to slack
def post_to_slack():
    for result in result_set:
        #print(result.text)
        score = sentiment_analysis(result.text)
        txt_slack = result.text + " " + score
        slack_data = {'text': txt_slack}
        
        # Post to slack
        requests.post(url=webhook_url, json = slack_data)



if __name__ == '__main__':
    post_to_postgre()
    post_to_slack()
