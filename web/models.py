from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from django_resized import ResizedImageField
from django.core.validators import MaxValueValidator, MinValueValidator



class Country(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.title}"
    
    class Meta: 
        verbose_name = "Страна"
        verbose_name_plural = "Страны"



class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.country.title})"


    class Meta: 
        verbose_name = "Город"
        verbose_name_plural = "Городы"



class Account(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    telegram_id = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self): 
        return f"{self.user.username}"

    class Meta: 
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"



class Category(models.Model): 
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=250)
    priority = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.title}"

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_ru)
        super(Category, self).save(*args, **kwargs)


    @property
    def total_product(self):
        products = Product.objects.filter(drop=False, category=self).count()
        return products

    @property
    def total_subcategory(self): 
        subcategories = SubCategory.objects.filter(category=self).count()
        return subcategories


    class Meta: 
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('priority',)



class SubCategory(models.Model): 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    priority = models.IntegerField()
    slug = models.CharField(max_length=255)

    
    def __str__(self) -> str:
        return f"{self.title} ({self.category.title})"

    
    @property
    def total_product(self):
        products = Product.objects.filter(drop=False, subcategory=self,).count()
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



class Product(models.Model): 
    category  = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=255)
    priority = models.IntegerField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)

    # ! Discount
    discount = models.IntegerField(default=0, validators=[MaxValueValidator(100),MinValueValidator(0)])
    discount_fk = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)

    drop = models.BooleanField(default=False)
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="web/products/300x300/")
    img_full = ResizedImageField(size=[600,600], quality=100, upload_to="web/products/600x600/")
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} ({self.category.title}): {self.price} UZS"


    class Meta: 
        verbose_name = "Наименование"
        verbose_name_plural = "Наименовании"
        ordering = ('priority',)



class ProductImage(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img_min = ResizedImageField(size=[300,300], quality=100, upload_to="web/products/300x300/")
    img_full = ResizedImageField(size=[600,600], quality=100, upload_to="web/products/600x600/")


    def __str__(self):
        return f"Фото: {self.product.title}"


    class Meta: 
        verbose_name = "Фото продукт"
        verbose_name_plural = "Фото пр"
        ordering = ('priority',)



class Slider(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    img_min = ResizedImageField(size=[300, 300], quality=100, upload_to=f"web/sliders/700x300/",  null=True, blank=True)
    img_max = ResizedImageField(size=[1200, 500], quality=100, upload_to=f"web/sliders/1200x500/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"