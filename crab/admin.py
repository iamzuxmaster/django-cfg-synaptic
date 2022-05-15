from django.contrib import admin
from .models import Moderator, Order, OrderType, OrderItem
# Register your models here.
admin.site.register(Moderator)
admin.site.register(Order)
admin.site.register(OrderType)
admin.site.register(OrderItem)