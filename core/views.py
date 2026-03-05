from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
from rest_framework.decorators import api_view
from rest_framework.response import Response

def health_check(request):
    return JsonResponse({"message": "Health check successful!"})

