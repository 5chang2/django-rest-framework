# django rest framework

## 참고
https://medium.com/wasd/restful-api-in-django-16fc3fb1a238

## 설치

- `pip install djangorestframework`

- `settings.py` 에 추가

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',
    'rest_framework',
]
```

## 모델정의

- `models.py`

```python
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
```

## Serializers 생성

- 지금까지 작성한 장고 서버의 경우 `사용자`가 보기 편하게 요청에 대한 응답을 처리해 주었다.
- render()함수를 통해서 views.py에서 만들어진 `Queryset <Post>` 을 넘기고 이를 HTML 파일에서 출력해주었다.

- API 서버는 사용자가 보기 편하게 응답을 해주는것이 아닌 데이터만 리턴해준다.
- HTML을 리턴 하지 않고 요청에 대한 데이이터만 json 형식으로 리턴한다.
- 이 과정을 처리해주는것이 rest framework에서 Serializers가 하는 역할이다.

- `posts/serializers.py

```python
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
```

## urls.py
```python
# project/urls.py
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
]

#posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_create),
    path('<int:id>/', views.read_update_delete),
]
```

## 코드작성

- views.py

```python
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
```