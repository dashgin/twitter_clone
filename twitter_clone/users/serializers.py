from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='api:user-detail',
        lookup_field='username'
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'name',
            'bio',
            'website',
            'date_joined',
            'url',
        ]

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("Joined %B %Y")
    # def get_follower_count(self, user):
    #     return 0
