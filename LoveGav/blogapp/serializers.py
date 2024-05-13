from django.shortcuts import get_object_or_404
from rest_framework import serializers

from blogapp.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author',)

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        default=None
    )

    def validate_post(self, value):
        post_id = self.context['view'].kwargs['pk']
        return get_object_or_404(Post, pk=post_id)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post', 'author')