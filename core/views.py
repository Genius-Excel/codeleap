from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer, PostUpdateSerializer



def health_check(request):
    """
    Health check endpoint for service availability monitoring.

    This endpoint is used to verify that the application is running and able
    to respond to HTTP requests. It can be used by load balancers, monitoring
    systems, or uptime checks.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the service health status.

    Response Example:
        {
            "message": "Health check successful!"
        }

    Status Codes:
        200 OK: The service is running and reachable.
    """
    return JsonResponse({"message": "Health check successful!"})


@api_view(["GET", "POST"])
def retrieve_and_create_posts(request):
    """
    Retrieve a list of posts or create a new post.

    This endpoint supports retrieving all posts or creating a new post
    in the system depending on the HTTP method used.

    Endpoint:
        /careers/

    Methods:
        GET:
            Retrieve a list of all posts ordered by creation date (latest first).

        POST:
            Create a new post using the provided request payload.

    Args:
        request (Request): The HTTP request object containing metadata,
            query parameters, and request body.

    Request Body (POST):
        JSON object containing the fields required to create a Post.

    Returns:
        Response:
            GET:
                Returns a list of serialized posts.

            POST:
                Returns the created post object if validation succeeds.

    Response Examples:
        GET:
        [
            {
                "id": 1,
                "title": "Software Engineer",
                "description": "Job description...",
                "created_datetime": "2026-03-05T10:30:00Z"
            }
        ]

        POST (Success):
        {
            "id": 2,
            "title": "Backend Developer",
            "description": "Job description...",
            "created_datetime": "2026-03-05T11:00:00Z"
        }

    Status Codes:
        200 OK:
            Returned for successful GET requests.

        201 Created:
            Returned when a post is successfully created.

        400 Bad Request:
            Returned when the request payload fails validation.
    """

    if request.method == "GET":
        posts = Post.objects.all().order_by("-created_datetime")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH", "DELETE"])
def update_or_delete_post(request, post_id):
    """
    Update or delete a specific post.

    This endpoint allows partial updates to an existing post or deletion
    of a post using its unique identifier.

    Endpoint:
        /careers/{post_id}/

    Methods:
        PATCH:
            Partially update fields of an existing post.

        DELETE:
            Permanently delete a post from the system.

    Args:
        request (Request): The HTTP request object containing metadata
            and request payload.
        post_id (int): Unique identifier of the post.

    Request Body (PATCH):
        JSON object containing one or more fields to update.

    Returns:
        Response:
            PATCH:
                Returns the updated post object after a successful update.

            DELETE:
                Returns an empty response indicating successful deletion.

    Response Examples:
        PATCH (Success):
        {
            "id": 1,
            "title": "Senior Backend Engineer",
            "description": "Updated job description...",
            "created_datetime": "2026-03-05T10:30:00Z"
        }

        Error (Post Not Found):
        {
            "detail": "Post not found"
        }

    Status Codes:
        200 OK:
            Returned when a post is successfully updated.

        204 No Content:
            Returned when a post is successfully deleted.

        400 Bad Request:
            Returned when the request payload fails validation.

        404 Not Found:
            Returned when the specified post does not exist.
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
