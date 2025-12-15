from django.db import models
import uuid
# Create your models here.


# ---------------------------------
# Company and Services
# ---------------------------------
class CompanyServices(models.Model):
    ServiceName = models.CharField(max_length=100)
    ServiceDescription = models.TextField()
    ServiceImage = models.ImageField(upload_to='services/')
    def __str__(self):
        return self.ServiceName

class CompanyInfo(models.Model):
    key = models.CharField(max_length=100, unique=True)  # مثال: location, work_hours, about_us
    value = models.TextField()

    def __str__(self):
        return self.key





# ---------------------------------
# Product Related
# ---------------------------------

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class ProductStatus(models.IntegerChoices):
    AVAILABLE = 1, "AVAILABLE"
    NOT_AVAILABLE = 2, "UNDER ORDER"


class ProductMaterial(models.Model):
    name = models.CharField(max_length=120)
    def __str__(self):
        return self.name

class ProductSize(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    main_image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    state = models.IntegerField(choices=ProductStatus.choices, default=ProductStatus.AVAILABLE)
    size = models.ManyToManyField('ProductSize', blank=True, related_name='products')
    material = models.ManyToManyField('ProductMaterial', blank=True, related_name='products')

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"


# ---------------------------------
# Email Verification
# ---------------------------------


class PendingEmail(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class ConfirmedEmail(models.Model):
    email = models.EmailField(unique=True)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email