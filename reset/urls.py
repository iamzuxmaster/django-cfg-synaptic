from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.index),
    path("email/", views.reset_email, name="reset_password_send"),
    path("<str:hash>/create/", views.reset_password_create, name="reset_password_create"),
    path("<str:hash>/", views.reset_password),
]