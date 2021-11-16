# Twitter-Slack Data Pipeline Project

In this project, my twitter scraper gathers tweets and initially stores them in a MongoDB databse.  The weets are cleaned and pushed onto a custom PostgreSQL databse. The cleaned tweets are then extracted and streamed to our Slack channel. The data pipeline is put together using docker-compose.
