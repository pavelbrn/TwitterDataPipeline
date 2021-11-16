import sqlalchemy as dbase
import json
import requests



webhook_url = "https://hooks.slack.com/services/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"

# when running locally then use ==> 0.0.0.0:5555/postgreCOMP  inside container==> postgresdb:5432
engine = dbase.create_engine('postgresql://pavel:123@0.0.0.0:5555/postgreCOMP', echo=False)

connection = engine.connect()
metadata = dbase.MetaData()
tweets = dbase.Table('tweets', metadata, autoload=True, autoload_with=engine)

query = dbase.select([tweets])
result_pr = connection.execute(query)
result_set = result_pr.fetchall()
a = result_set[:10]
#print(type(a))

for result in result_set:
    #print(result.text)
    txt_slack = result.text
    slack_data = {'text': txt_slack}
    requests.post(url=webhook_url, json = slack_data)

