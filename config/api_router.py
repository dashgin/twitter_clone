from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from twitter_clone.tweets.views import TweetViewSet
from twitter_clone.users.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("tweets", TweetViewSet)

app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="Twitter clone API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@twitter.clone"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger UI
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # DRF auth token
    path("auth-token/", obtain_auth_token),

    path("users/", include("twitter_clone.users.urls", namespace="users")),

    path("tweets/", include("twitter_clone.tweets.urls", namespace="tweets")),
]
urlpatterns += router.urls
