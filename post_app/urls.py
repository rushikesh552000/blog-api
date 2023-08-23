from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('api/posts/', AllPostDetailAPI.as_view(), name='posts'),
    path('api/posts/<int:pk>/', SinglePostDetailAPI.as_view(), name='single_posts'),

]