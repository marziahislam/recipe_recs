from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_recipe, name='recommend_recipe'),
]