from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, ChangePasswordSerializer
from twitter_clone.utils.permissions import IsSelfOrReadOnly


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = [IsSelfOrReadOnly]

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)



class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


register_view = RegisterView.as_view()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


login_view = MyObtainTokenPairView.as_view()


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsSelfOrReadOnly,)
    serializer_class = ChangePasswordSerializer
    lookup_field = 'username'

change_password_view = ChangePasswordView.as_view()


class FollowToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, *args, **kwargs):
        follower = self.request.user
        user = User.objects.get(username=self.kwargs['username'])
        message = "Not allowed"
        if follower != user and follower.is_authenticated:
            is_following = User.objects.follow_toggle(user=user, follower=follower)
            return Response({'following': is_following}, )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


follow_toggle_view = FollowToggleAPIView.as_view()
