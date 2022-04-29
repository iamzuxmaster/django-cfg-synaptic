from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from django_resized import ResizedImageField
from django.core.validators import MaxValueValidator, MinValueValidator



class Region(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.title_ru}"
    
    class Meta: 
        verbose_name = "Страна"
        verbose_name_plural = "Страны"



class Disctrict(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)    
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title_ru} ({self.region.title_ru})"


    class Meta: 
        verbose_name = "Город"
        verbose_name_plural = "Городы"



class Account(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    roles = [
        ("client", "Client"),
        ("moderator", "Moderator-Admin"),
        ("admin", "Controller"),
        ("superadmin", "SuperAdmin"),
    ]
    role = models.CharField(max_length=255, choices=roles)
    telegram_id = models.IntegerField(null=True, blank=True)
    telegram_langs = [
        ("ru", "Русские"),
        ("uz", "O'zbekcha"),
    ]
    telegram_lang = models.CharField(max_length=5, choices=telegram_langs, null=True, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self): 
        return f"{self.user.username}"

    class Meta: 
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"



class Category(models.Model): 
    img = ResizedImageField(size=[600,600], quality=100, upload_to="control/categories/", null=True, blank=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    slug = models.CharField(max_length=250)
    priority = models.IntegerField(default=0)

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title_ru}"

    class Meta: 
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('priority',)


    @property
    def total_products(self):
        products = Product.objects.filter(drop=False, category=self).count()
        return products

    @property
    def total_subcategories(self): 
        subcategories = SubCategory.objects.filter(category=self).count()
        return subcategories




class SubCategory(models.Model): 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    priority = models.IntegerField()
    slug = models.CharField(max_length=255)

    
    def __str__(self) -> str:
        return f"{self.title_ru} ({self.category.title_ru})"

    
    @property
    def total_products(self):
        products = Product.objects.filter(drop=False, subcategory=self).count()
        return products


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(SubCategory, self).save(*args, **kwargs)


    class Meta: 
        verbose_name = "ПодКатегория"
        verbose_name_plural = "ПодКатегории"
        ordering = ('priority',)


class Discount(models.Model):
    title = models.CharField(max_length=255)
    unit = models.IntegerField(default=0, validators=[MaxValueValidator(100),MinValueValidator(0)])

    
    def __str__(self):
        return f"{self.title}: {self.unit}%"


    class Meta: 
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    @property
    def total_product(self):
        return Product.objects.filter(drop=False, discount=self).count()


class Product(models.Model): 
    category  = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255)
    priority = models.IntegerField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)

    drop = models.BooleanField(default=False)
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="web/products/300x300/")
    img_full = ResizedImageField(size=[600,600], quality=100, upload_to="web/products/600x600/")
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title_ru} ({self.category.title_ru}): {self.price} UZS"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Product, self).save(*args, **kwargs)


    class Meta: 
        verbose_name = "Наименование"
        verbose_name_plural = "Наименовании"
        ordering = ('priority',)



class ProductImage(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="web/products/300x300/")
    img_full = ResizedImageField(size=[600,600], quality=100, upload_to="web/products/600x600/")


    def __str__(self):
        return f"Фото: {self.product.title_ru}"


    class Meta: 
        verbose_name = "Фото продукт"
        verbose_name_plural = "Фото продукты"

class Slider(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    content_uz = models.CharField(max_length=255)
    content_ru = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField(null=True, blank=True)
    img_min = ResizedImageField(size=[300, 300], quality=100, upload_to=f"web/sliders/700x300/",  null=True, blank=True)
    img_full = ResizedImageField(size=[1200, 500], quality=100, upload_to=f"web/sliders/1200x500/", null=True, blank=True)
    priority = models.IntegerField()
    slug = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title_ru}"

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Slider, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"
        
class Blog(models.Model): 
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    description_uz = models.TextField()
    description_ru = models.TextField(null=True, blank=True)
    img_full = ResizedImageField(size=[600, 600], quality=100, upload_to="blogs/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.title_ru}"
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Slider, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блог"

class OrderTypes(models.Model):
    title_ru = models.CharField(max_length=255)
    priority = models.IntegerField(default=0)
    color = models.CharField(max_length=255,null=True, blank=True)
    edit = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.title_ru}"
    
    class Meta:
        verbose_name = "Этап заказов"
        verbose_name_plural = "Этап заказов"

    @property
    def type_orders(self):
        return Order.objects.filter(ordertypes=self, checkout=True, complete=False)

    @property
    def type_orders_droped(self):
        return Order.objects.filter(ordertypes=self,drop=True)

    @property
    def type_orders_completed(self):
        return Order.objects.filter(ordertypes=self, drop=True, complete=True, checkout=True)


class Order(models.Model): 
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ordertypes = models.ForeignKey(OrderTypes, on_delete=models.PROTECT, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    ordertypes_comment = models.TextField(null=True, blank=True)
    checkout = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    drop = models.BooleanField(default=False)

    
    def __str__(self) -> str:
        return f"{self.account}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    @property
    def total_items(self):
        quantities = 0
        for orderitem in OrderItem.objects.filter(order=self):
            quantities += orderitem.quantity
        return quantities

    @property
    def total_price(self):
        price = 0
        for orderitem in OrderItem.objects.filter(order=self):
            price += orderitem.total_price
        return price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    
    def __str__(self) -> str:
        return f"{self.order} {self.product.title_ru}"
    
    class Meta:
        verbose_name = "Товар на Заказ"
        verbose_name_plural = "Товары на Заказ"

    @property
    def total_price(self): 
        return self.product.price * self.quantity


class Office(models.Model):
    title_ru = models.CharField(max_length=255)
    category_imgs = models.BooleanField(default=False)
    description_uz  = models.TextField(max_length=255)
    description_ru  = models.TextField(max_length=255)
    currency = models.CharField(max_length=255, null=True, blank=True, default="UZS")
    map = models.TextField(null=True, blank=True)
    logo = ResizedImageField(size=[600, 600], quality=100, upload_to=f"control/office/")
    phone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.title_ru}"
    
    class Meta:
        verbose_name = "Инфо"
        verbose_name_plural = "Инфо"

class Contact(models.Model): 
    fio = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField()
    

class OfficePhone(models.Model):
    title = models.CharField(max_length=255)
    phone = models.IntegerField()
class OfficeEmail(models.Model):
    title = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
class OfficeAddress(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField()