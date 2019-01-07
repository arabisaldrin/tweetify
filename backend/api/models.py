from django.db import models
from django.contrib.auth.models import User


class FilterGroup(models.Model):
    name = models.TextField(blank=False)
    description = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)


class FilterItem(models.Model):
    content = models.TextField(blank=False)
    group = models.ForeignKey(
        FilterGroup, on_delete=models.CASCADE, related_name="items")
    is_active = models.BooleanField(default=True)


class Tweet(models.Model):
    id_str = models.TextField()
    content = models.TextField()
    full_content = models.TextField()
    user_name = models.TextField()
    user_image_url = models.TextField()
    user_description = models.TextField()
    polarity = models.FloatField()
    subjectivity = models.FloatField()
    retweet_count = models.BigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    user_location = models.TextField(null=True)
    coordnates = models.TextField(null=True)
    geo_location = models.TextField(null=True)
    screen_name = models.TextField()
    user_followers_count = models.BigIntegerField()
    streamer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
