from django.urls import path
from . import views
urlpatterns = [
    path('', views.crab_index,name='crab_index')
]