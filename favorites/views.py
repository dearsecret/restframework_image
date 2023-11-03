from .serializers import FavoriteSerializer
from .models import Favorite
from chats.models import Chat
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class FavoriteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data)


class ToggleFavorite(APIView):
    permission_classes = [IsAuthenticated]

    def get_post(self, pk):
        try:
            return Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            raise NotFound

    def get_favorite(self, user):
        try:
            return Favorite.objects.get_or_create(user=user)
        except Favorite.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        post = self.get_post(pk)
        favorite, created = self.get_favorite(request.user)
        if favorite.posts.filter(pk=post.pk).exists():
            favorite.posts.remove(post)
            return Response({"favorite": False, "count": post.favorites.count()})
        else:
            favorite.posts.add(post)
            return Response({"favorite": True, "count": post.favorites.count()})
