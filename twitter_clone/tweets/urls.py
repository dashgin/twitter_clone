from django.urls import path

from .views import like_toggle_view, retweet_view

app_name = "tweets"
urlpatterns = [
    path('<int:pk>/like/', like_toggle_view),
    path('<int:pk>/retweet/', retweet_view)
]
