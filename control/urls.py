from django.urls import path 
from . import views

urlpatterns = [
    path("", views.control_index, name="control_index"),
    
    # Categories
    path("categories/", views.control_categories_all, name="control_categories_all"),
    path("category/add/", views.control_categories_add, name="control_category_add"),
        path("category/create/", views.control_categories_create, name="control_category_create"),
        path("category/edit/", views.control_categories_edit, name="control_category_edit"),
        path("categories/delete/", views.control_categories_delete, name="control_category_delete"),
    path("category/<str:slug>/", views.control_categories_detail, name="control_category_detail"),
] 