from django.urls import path, include

urlpatterns = [
    path('control/', include("control.urls"))
]