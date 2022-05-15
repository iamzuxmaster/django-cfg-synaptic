from django.db import models
from control.models import Account, Product
from django_resized import ResizedImageField


with_orderitem = False

class Moderator(models.Model):
    profile_img = ResizedImageField(size=[600, 600], quality=100, upload_to='moderators/img/', null=True, blank=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='moderator')
    birthday = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def total_orders(self):
        orders = Order.objects.filter(moderator=self, checkout=True)
        return orders.count()

    def total_complete_orders(self):
        orders = Order.objects.filter(moderator=self, checkout=True, complete=True)
        return orders.count()
    
    def total_canceled_orders(self):
        orders = Order.objects.filter(moderator=self, drop=True)
        return orders.count()


    def __str__(self) -> str:
        return f"Модератор: {self.account.user.first_name}"

    class Meta:
        verbose_name = "Модератор"
        verbose_name_plural = "Модераторы"


class OrderType(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"Этап: {self.title}"

    class Meta:
        verbose_name = "Этап"
        verbose_name_plural = "Этапы"



class Order(models.Model):
    uuid = models.CharField(max_length=255, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    fio = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    checkout = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    drop = models.BooleanField(default=False)
    order_type = models.ForeignKey(OrderType, on_delete=models.PROTECT, null=True, blank=True)
    moderator = models.ForeignKey(Moderator, on_delete=models.SET_NULL, null=True, blank=True)

    complete = models.BooleanField(default=False)

    date_checkout = models.DateTimeField(null=True, blank=True)

    def total_item(self):
        items = OrderItem.objects.filter(order=self)
        return items.count()
    
    def total_sum(self):
        items = OrderItem.objects.filter(order=self)
        sum = 0
        for item in items:
            sum += item.total_sum()
        return sum

    def __str__(self) -> str:
        return f"Заказ: {self.uuid} - {'модератор:' + {self.moderator.account.user.first_name if self.moderator.account.user.first_name else 'Нет'} if self.checkout else 'Не заказал'}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ('date_checkout',)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def total_sum(self):
        sum = self.quantity * self.product.price
        return sum

    def __str__(self) -> str:
        return f"Товар на Заказ: {self.order.uuid}"

    class Meta:
        verbose_name = "Товар на Заказ"
        verbose_name_plural = "Товары на Заказ"

class Task(models.Model):
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='task_sender_account')
    reader_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='task_reader_account')
    title = models.CharField(max_length=255)
    description = models.TextField()
    istask = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    date_complete = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Задание: {self.title} ({self.sender_account.user.username} -> {self.reader_account.user.username})"

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задании"