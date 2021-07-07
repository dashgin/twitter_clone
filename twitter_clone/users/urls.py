from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    follow_toggle_view,
    login_view,
    register_view,
    change_password_view
)

app_name = "users"

urlpatterns = [
    path('signup/', register_view, name='register'),
    path('login/', login_view, name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<str:username>/change-password', change_password_view),
    path('<str:username>/follow', follow_toggle_view),
]
