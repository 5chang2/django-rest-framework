# from django.shortcuts import render
# render를 해줄일이 없어 필요 없음
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
# Create your views here.

@api_view(['GET','POST'])
def list_create(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_REQUEST)

@api_view(['GET','PUT','DELETE'])
def read_update_delete(request,id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)