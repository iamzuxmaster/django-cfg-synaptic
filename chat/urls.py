from django.urls import path, include
from . import views
urlpatterns = [
    path("all/messages/", views.control_chat_all_messages)
]