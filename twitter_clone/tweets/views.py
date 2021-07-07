from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Tweet
from .serializers import TweetSerializer
from django.shortcuts import get_object_or_404

from twitter_clone.utils.permissions import IsOwnerOrReadOnly


class TweetViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, *args, **kwargs):
        user = self.request.user
        tweet = Tweet.objects.get(pk=int(self.kwargs['pk']))
        message = "Not allowed"
        if user.is_authenticated:
            is_liked = Tweet.objects.like_toggle(user, tweet)
            return Response({'liked': is_liked}, )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)


like_toggle_view = LikeToggleAPIView.as_view()


class RetweetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        parent = get_object_or_404(Tweet, pk=int(self.kwargs['pk']))
        if user.is_authenticated:
            data = {'user_id': user.id, 'parent_id': parent.id, 'content': parent.content, 'is_retweet': True}
            serializer = TweetSerializer(data=data, context={'request': request})
            print(serializer)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


retweet_view = RetweetAPIView.as_view()
