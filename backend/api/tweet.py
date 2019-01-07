import tweepy
from textblob import TextBlob
import json
import time
from requests.exceptions import ConnectionError
from .models import FilterGroup, Tweet
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.serializers.json import DjangoJSONEncoder
from backend.api.models import User
from datetime import datetime, time
import json
import logging
import re
import pytz

# Sir Rajat Twitter API Credentials
TWITTER_APP_KEY = 'NbIJpPFfD1Utc3rniAZb6LEV0'
TWITTER_APP_SECRET = 'a68tIE0Br5vGjZ1WSqisSCiHj6oBHy2VmusECNfMt9YjoQWQHc'
TWITTER_KEY = '1052482036764618757-2bac0mOpZz1MBWISzn4Bskftxf3Are'
TWITTER_SECRET = '35yKKMHGmvbx0wpnl4fuTrx2eOvPNiuiFfx7Pf3xtO6Ny'


class IOTweetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('ws:connected')
        self.stream_manager = StreamManager()
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user = User.objects.get(pk=self.user_id)
        self.room_group_name = 'tweet_streams_%s' % self.user_id
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        print('ws:disconnected')
        self.stream_manager.cancel()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print('ws:receive')
        data = json.loads(text_data)
        if data['type'] == 'cmd':
            await self.execute_command(data['command'])
            return

        message = data['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_message',
                'message': message
            }
        )

    async def broadcast_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=message)

    async def execute_command(self, cmd):
        if(cmd == 'start'):
            self.stream_manager.start(self.user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_message',
                    'message': json.dumps({
                        'type': 'cmd-response',
                        'cmd': 'start',
                        'result': self.stream_manager.listening
                    })
                }
            )
        elif cmd == 'stop':
            self.stream_manager.cancel()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_message',
                    'message': json.dumps({
                        'type': 'cmd-response',
                        'cmd': 'stop',
                        'result': not self.stream_manager.listening
                    })
                }
            )
        elif cmd == 'restart':
            self.stream_manager.restart()


class StreamListener(tweepy.StreamListener):
    channel_layer = get_channel_layer()

    def set_user(self, user):
        self.user = user

    def on_status(self, status):
        if status.retweeted:
            return

        full_text = status.text
        try:
            try:
                full_text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                full_text = status.extended_tweet["full_text"]
        except AttributeError:
            pass

        # sentiment analysis
        blob = TextBlob(' '.join(re.sub(
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", full_text).split()))  # clean text content first
        sent = blob.sentiment

        geo = json.dumps(
            status.geo) if status.geo is not None else None
        coords = json.dumps(
            status.coordinates) if status.coordinates is not None else None

        tz = pytz.timezone('Asia/Manila')
        tweet_date = tz.localize(status.created_at)
        data = {
            "id_str": status.id_str,
            "content": status.text,
            "full_content": full_text,
            "user_name": status.user.name,
            "user_image_url": status.user.profile_image_url,
            "user_description": status.user.description,
            "polarity": sent.polarity,
            "subjectivity": sent.subjectivity,
            "retweet_count": status.retweet_count,
            "created_at": status.created_at,
            "created_at": tweet_date,
            "user_location": status.user.location,
            "coordnates": coords,
            "geo_location": geo,
            "screen_name": status.user.screen_name,
            "user_followers_count": status.user.followers_count
        }

        tweet = Tweet(**data, streamer=self.user)
        tweet.save()

        # send to websocket
        async_to_sync(self.channel_layer.group_send)(
            "tweet_streams_%s" % self.user.pk, {
                "type": "broadcast_message",
                "message": json.dumps(
                    {
                        "type": 'tweet',
                        "data": data
                    },
                    sort_keys=True,
                    cls=DjangoJSONEncoder)
            })

        # append to file consumer
        row = ''

        for c in list(data.values()):
            row += '%s\t' % ('' if c is None else c)

        row += "\r\n"

        with open("tweets.txt", "a+") as f:
            f.write(row)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)


class StreamManager():

    stream = None
    listening = False

    def start(self, user):
        print('stream:start')
        self.user = user
        stream_listener = StreamListener()
        stream_listener.set_user(user)
        if not self.listening:
            filter_set = []
            groups = FilterGroup.objects.filter(user=user, is_active=True)
            for group in groups:
                items = group.items.filter(
                    is_active=True).values_list('content', flat=True)
                filter_set.extend(items)

            print(filter_set)
            self.stream = tweepy.Stream(
                auth=api.auth, listener=stream_listener, tweet_mode='extended')
            self.stream.filter(track=filter_set, is_async=True)
            self.listening = True

        return self.listening

    def restart(self):
        if self.listening:
            self.cancel()
            self.start(self.user)

    def cancel(self):
        print('stream:stop')
        if self.stream:
            self.stream.disconnect()
            self.listening = False
