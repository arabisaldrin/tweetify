from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import FilterItem, FilterGroup, User, Tweet
from django.contrib.auth.hashers import make_password


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'username', 'email',
                  'is_superuser', 'is_staff', 'is_active')
        write_only_fields = ('password',)


class FilterItemSerializer(ModelSerializer):

    class Meta:
        model = FilterItem
        fields = ('pk', 'content', 'group')


class FilterGroupSerializer(ModelSerializer):
    items = FilterItemSerializer(many=True, read_only=True)

    class Meta:
        model = FilterGroup
        fields = ('pk', 'name', 'description', 'items', 'user')


class TweetSerializer(ModelSerializer):

    class Meta:
        model = Tweet
        fields = ('id_str',
                  'content',
                  'full_content',
                  'user_name',
                  'user_image_url',
                  'user_description',
                  'polarity',
                  'subjectivity',
                  'retweet_count',
                  'created_at',
                  'created_at',
                  'user_location',
                  'coordnates',
                  'geo_location',
                  'screen_name',
                  'user_followers_count')
