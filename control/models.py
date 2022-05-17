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
        ("moderator", "Moderator"),
        ("admin", "Admin"),
        ("superadmin", "SuperAdmin"),
        ("developer", "Developer"),
    ]
    role = models.CharField(max_length=255, choices=roles, default="client")
    telegram_id = models.IntegerField(null=True, blank=True)
    telegram_langs = [
        ("ru", "Русские"),
        ("uz", "O'zbekcha"),
    ]
    secret_key  = models.CharField(max_length=255, null=True, blank=True)
    telegram_lang = models.CharField(max_length=5, choices=telegram_langs, null=True, blank=True)
    verified = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
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

class Office(models.Model):
    title_ru = models.CharField(max_length=255)
    description_uz  = models.TextField(max_length=255)
    description_ru  = models.TextField(max_length=255)
    currency = models.CharField(max_length=255, null=True, blank=True, default="UZS")
    map = models.TextField(null=True, blank=True)
    logo = ResizedImageField(size=[600, 600], quality=100, upload_to=f"control/office/")
    phone = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    # For Developers
    category_imgs = models.BooleanField(default=False)
    main_color = models.CharField(max_length=255, null=True, blank=True)
    
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

class NotificationType(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255) 

class Notification(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.ForeignKey(NotificationType, on_delete=models.SET_NULL, null=True, blank=True)
    readed = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    content = models.TextField()

class Room(models.Model):
    account_a = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="room_account_a")
    account_b = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="room_account_b")
    uuid = models.CharField(max_length=250, null=True, blank=True)

class Message(models.Model): 
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
