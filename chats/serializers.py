from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from .models import Chat, Comment
from users.serializers import GenderSerializer


class CommentSerializer(ModelSerializer):
    is_owner = SerializerMethodField()
    is_writer = SerializerMethodField()
    gender = SerializerMethodField()
    replies = SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "pk",
            "gender",
            "content",
            "is_owner",
            "is_writer",
            "created_at",
            "parent",
            "replies",
        )
        write_only_fields = ("author",)

    def get_replies(self, comment):
        serializer = self.__class__(comment.replies, many=True)
        serializer.bind("", self)
        return serializer.data

    def get_gender(self, comment):
        return comment.author.discrimination

    def get_is_owner(self, comment):
        request = self.context.get("request")
        if request:
            if request.user.pk == comment.author.pk:
                return True
        return False

    def get_is_writer(self, comment):
        request = self.context.get("request")
        if request:
            if comment.comment_post.writer.pk == comment.author.pk:
                return True
        return False


class ChatSerializer(ModelSerializer):
    is_owner = SerializerMethodField()
    is_favorite = SerializerMethodField()
    count_comment = SerializerMethodField()
    count_likes = SerializerMethodField()
    count_dislikes = SerializerMethodField()
    comments = SerializerMethodField()
    gender = SerializerMethodField()
    prefer = SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            "prefer",
            "pk",
            "title",
            "content",
            "image",
            "views",
            "is_owner",
            "is_favorite",
            "gender",
            "count_comment",
            "count_likes",
            "count_dislikes",
            "created_at",
            "comments",
        )
        write_only_fields = ("writer",)

    def get_prefer(self, chat):
        request = self.context.get("request")
        if chat.likes.filter(pk=request.user.pk).exists():
            return True
        elif chat.dislikes.filter(pk=request.user.pk).exists():
            return False
        else:
            return None

    def get_gender(self, chat):
        return chat.writer.discrimination

    def get_count_comment(self, chat):
        return chat.count_comment()

    def get_count_likes(self, chat):
        return chat.count_likes()

    def get_count_dislikes(self, chat):
        return chat.count_dislikes()

    def get_is_owner(self, chat):
        request = self.context.get("request")
        if request:
            if request.user.pk == chat.writer.pk:
                return True
        return False

    def get_is_favorite(self, chat):
        request = self.context.get("request")
        if request:
            if chat.favorites.filter(user=request.user).exists():
                return True
            else:
                return False
        else:
            return False

    def get_comments(self, chat):
        serializer = CommentSerializer(
            chat.comments.filter(parent=None), many=True, context=self.context
        )
        return serializer.data


class ChatListSerializer(ModelSerializer):
    count_comment = SerializerMethodField()
    count_likes = SerializerMethodField()
    count_dislikes = SerializerMethodField()
    writer = GenderSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = (
            "pk",
            "title",
            "image",
            "count_comment",
            "views",
            "created_at",
            "count_likes",
            "count_dislikes",
            "writer",
        )

    def get_count_comment(self, chat):
        return chat.count_comment()

    def get_count_likes(self, chat):
        return chat.count_likes()

    def get_count_dislikes(self, chat):
        return chat.count_dislikes()


class PostChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            "pk",
            "title",
            "image",
            "content",
            "created_at",
        )
