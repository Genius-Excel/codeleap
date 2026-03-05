from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('', views.posts_collection, name='posts-collection'),
    path('<int:post_id>/', views.post_update, name='post-update'),
]