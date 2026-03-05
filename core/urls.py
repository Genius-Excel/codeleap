from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('', views.retrieve_and_create_posts, name='posts-collection'),
    path('<int:post_id>/', views.update_or_delete_post, name='post-update'),
]