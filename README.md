# tweet-alert

A simple twitter live streamer application that uses [Nuxt.js](https://nuxtjs.org/) as front end framework and backed with the powerfull [Django](https://www.djangoproject.com/)

# Feature

- Live stream of tweets using [tweepy](http://www.tweepy.org/) then rendered at client trough WebSocket
- Filtering module where you can specify some tweepy tracks that includes grouping
- Role based, filtering is user specific using simple authentication/login module
- Sentiment analysis using python [TextBlob](https://textblob.readthedocs.io/en/dev/)
- Real time sentiment analysis graph
- Start and stop live stream

# Requirements

- [Redis](https://hub.docker.com/_/redis/) for python websocket channel layering
- [Postgres](https://hub.docker.com/_/postgres/) as database
- [Yarn](https://yarnpkg.com/en/) dependency manager (Dev)
- [pipenv](https://pypi.org/project/pipenv/) for python virtual environemnt

# Instruction

- Install dependencies using "pipenv install and yarn install"
- Start postgres and redis at default ports
- Create postgres user (You can use django manage command "pipenv run python manage.py createsuperuser")
- Start the nuxt server using "yarn start"
