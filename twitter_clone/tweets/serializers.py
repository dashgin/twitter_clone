from django.utils.timesince import timesince
from rest_framework import serializers

from .models import Tweet

from twitter_clone.users.serializers import UserSerializer


class TweetSerializer(serializers.ModelSerializer):
    # user = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)
    parent_id = serializers.CharField(write_only=True, required=False)
    time_since = serializers.SerializerMethodField()
    date_display = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    did_retweeted = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='api:tweet-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Tweet
        fields = [
            'id', 'user', 'parent_id', 'parent', 'content', 'created_at', 'time_since',
            'date_display', 'did_like', 'did_retweeted', 'likes_count', 'url'
        ]

    def get_time_since(self, obj):
        return timesince(obj.created_at)

    def get_date_display(self, obj):
        return obj.created_at.strftime("%I:%M %p · %d %b %y")

    def get_likes_count(self, obj):
        return obj.likes.all().count()

    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                return True
        return False

    def get_did_retweeted(self, obj):
        request = self.context.get("request")
        user = request.user
        if obj.parent is not None:
            return True
        return False

    # extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}
