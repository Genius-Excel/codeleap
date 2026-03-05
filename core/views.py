from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
from rest_framework.decorators import api_view
from rest_framework.response import Response

def health_check(request):
    return JsonResponse({"message": "Health check successful!"})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializer, PostUpdateSerializer


@api_view(["GET", "POST"])
def posts_collection(request):
    """
    This view handles both GET and POST requests for the collection of posts.
    GET /careers/ - Retrieve a list of all posts.
    POST /careers/ - Create a new post with the provided data.
    
    """

    if request.method == "GET":
        posts = Post.objects.all().filter().order_by("-created_datetime")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "DELETE"])
def post_update(request, post_id):
    """
    PATCH /careers/{id}/
    DELETE /careers/{id}/
    """

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {"detail": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "PATCH":
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(PostSerializer(post).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
