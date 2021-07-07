from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from .validators import validate_f_word

User = get_user_model()


class TweetManager(models.Manager):
    # def retweet(self, user, parent_obj):
    #     if parent_obj.parent:
    #         og_parent = parent_obj.parent
    #     else:
    #         og_parent = parent_obj
    #     qs = self.get_queryset().filter(user=user, parent=og_parent)
    #     if qs.exists():
    #         return None
    #     obj = self.model(parent=parent_obj, user=user, content=parent_obj.content)
    #     obj.save()
    #     return obj

    def like_toggle(self, user, tweet_obj):
        if user in tweet_obj.likes.all():
            is_liked = False
            tweet_obj.likes.remove(user)
        else:
            is_liked = True
            tweet_obj.likes.add(user)
        return is_liked


class Tweet(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=150, validators=[validate_f_word])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(to='Hashtag', blank=True)
    likes = models.ManyToManyField(User, related_name='tweet_likes', blank=True)
    is_retweet = models.BooleanField(default=False)
    objects = TweetManager()

    def __str__(self):
        return str(self.user) + str(self.id)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('api:tweet-detail', kwargs={'pk': self.id})

    def get_parent(self):
        if self.parent:
            parent = self.parent
            return parent
        else:
            return None

    def get_retweets(self):
        parent = self.get_parent()
        qs = Tweet.objects.filter(parent=parent)
        qs_parent = Tweet.objects.filter(pk=parent.pk)
        return qs | qs_parent


class Hashtag(models.Model):
    name = models.CharField(max_length=120, validators=[validate_f_word])

    def __str__(self):
        return self.name
#
#     def get_absolute_url(self):
#         return reverse("hashtag", kwargs={"tag": self.name})
#
#     def tag_tweets(self):
#         return Tweet.objects.filter(content__icontains='#' + self.name)
