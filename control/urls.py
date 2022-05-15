from django.urls import path, include
from . import views
from .api import api as control_api

urlpatterns = [
    path("", views.control_index, name="control_index"),
    path("chat/", include("chat.urls")),
    path("api/", control_api.urls),
    path("logout/", views.log_out, name="control_logout"),
    path("login/", views.log_in, name="control_login"),
        path("signin/", views.sign_in, name="control_signin"),

    # Categories 
    path("categories/", views.control_categories_all, name="control_categories_all"),
    path("category/add/", views.control_categories_add, name="control_category_add"),
        path("category_add/", views.control_subcategories_category_add),
        path("category/create/", views.control_categories_create, name="control_category_create"),
        path("category/edit/", views.control_categories_edit, name="control_category_edit"),
        path("category/delete/", views.control_categories_delete, name="control_category_delete"),
    path("category/<str:slug>/", views.control_categories_detail, name="control_category_detail"),

    # SubCategories 
    path("subcategories/", views.control_subcategories_all, name="control_subcategories_all"),
    path("subcategory/add/", views.control_subcategories_add, name="control_subcategory_add"),
        path("subcategory_add/", views.control_products_subcategory_add),
        path("subcategory/create/", views.control_subcategories_create, name="control_subcategory_create"),
        path("subcategory/edit/", views.control_subcategories_edit, name="control_subcategory_edit"),
        path("subcategory/delete/", views.control_subcategories_delete, name="control_subcategory_delete"),
    path("subcategory/<str:slug>/", views.control_subcategories_detail, name="control_subcategory_detail"),

    # Discounts
    path("discounts/", views.control_discounts_all, name="control_discounts_all"),
    path("discount/add/", views.control_discount_add, name="control_discount_add"),
        path("discount_add/", views.control_products_discount_add, name="control_discount_add"),
        path("discount/create/", views.control_discount_create, name="control_discount_create"),
        path("discount/edit/", views.control_discount_edit, name="control_discount_edit"),
        path("discount/delete/", views.control_discount_delete, name="control_discount_delete"),
    path("discount/<int:id>/", views.control_discount_detail, name="control_discount_detail"),
 
    # Products 
    path("products/", views.control_products_all, name="control_products_all"),
    path("product/add/", views.control_product_add, name="control_products_add"),
        path("product/image/add/", views.control_product_image_add, name="control_product_image_add"),
        path("product/image/delete/", views.control_product_image_delete, name="control_product_image_delete"),
        path("product/create/", views.control_product_create, name="control_products_create"),
        path("product/edit/", views.control_product_edit, name="control_products_edit"),
        path("product/delete/", views.control_product_delete, name="control_products_delete"),
    path("product/<str:slug>/", views.control_product_detail, name="control_products_detail"),

 
    # Sliders
    path("sliders/", views.control_sliders_all, name="control_sliders_all"),
    path("slider/add/", views.control_sliders_add, name="control_sliders_add"),
        path("slider/create/", views.control_sliders_create, name="control_sliders_create"), 
        path("slider/edit/", views.control_sliders_edit, name="control_sliders_edit"),
        path("slider/delete/", views.control_sliders_delete, name="control_sliders_delete"),
    path("slider/<slug:slug>/", views.control_sliders_detail, name="control_sliders_detail"),

    # News
    path("blogs/", views.control_blogs_all, name="control_blogs_all"),
    path("blog/add/", views.control_blog_add, name="control_blog_add"),
        path("blog/create/", views.control_blog_create, name="control_blog_create"), 
        path("blog/edit/", views.control_blog_edit, name="control_blog_edit"),
        path("blog/delete/", views.control_blog_delete, name="control_blog_delete"),
    path("blog/<int:id>/", views.control_blog_detail, name="control_blog_detail"),

    # Orders
    path("orders/", include("crab.urls")),
    path("accounts/", views.control_accounts, name="control_accounts"),
    path("admins/", views.control_admins, name="control_admins"),
    path("admin/add/", views.control_admins_add, name="control_admins_add"),
        path("admin/create/", views.control_admins_create, name="control_admins_create"),
        path("admin/edit/", views.control_admins_edit, name="control_admins_edit"),
        path("admin/delete/", views.control_admins_delete, name="control_admins_delete"),
    path("admin/<str:login>/", views.control_admins_detail, name="control_admins_detail"),


    path("aboutus/", views.control_aboutus, name="control_aboutus"),
        path("aboutus/edit/", views.control_aboutus_edit, name="control_aboutus_edit"),
        path("aboutus/phone/add/", views.control_aboutus_phone_add, name="control_aboutus_phone_add"),
        path("aboutus/email/add/", views.control_aboutus_email_add, name="control_aboutus_email_add"),
        path("aboutus/phone/delete/", views.control_aboutus_phone_delete, name="control_aboutus_phone_delete"),
        path("aboutus/email/delete/", views.control_aboutus_email_delete, name="control_aboutus_email_delete"),
    path("aboutus/address/add/", views.control_aboutus_address_add, name="control_aboutus_address_add"),

 ]      