from django.urls import path

from .views import like_toggle, retweet

app_name = "tweets"
urlpatterns = [
    path('<int:pk>/like/', like_toggle),
    path('<int:pk>/retweet/', retweet)
]
