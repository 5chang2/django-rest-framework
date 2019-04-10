from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at','updated_at',)