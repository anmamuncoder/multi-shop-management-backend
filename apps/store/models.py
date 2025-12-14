from django.db import models
from django.utils.text import slugify
# External 
from apps.base.models import BaseModel
from apps.base.utils import generate_unique_slug
from apps.accounts.models import User
# Internal
from .constants import CURRENCY_CHOICES,PRODUCT_IMAGE_UPLOAD_TO

# Create your models here.
class Shop(BaseModel):
    owner = models.OneToOneField(User,on_delete=models.PROTECT,null=True, limit_choices_to={'role': 'shop_owner'},related_name='shop')
    name = models.CharField(max_length=100)
    balance = models.BigIntegerField(default=0,editable=False)
    
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField()
    short_intro = models.TextField()

    logo = models.ImageField(upload_to="logo/",blank=True,null=True)
    banner = models.ImageField(upload_to="logo/",blank=True,null=True)
    cover_photo = models.ImageField(upload_to="logo/",blank=True,null=True)
    primary_color = models.CharField(max_length=20)

    policies = models.TextField()
    currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    total_sales = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Shop {self.name} - Owner {self.owner.email}"

    def save(self, *args, **kwargs):
        # Slug Auto Create
        if not self.slug:
            self.slug = generate_unique_slug(Shop,self.name,'slug')

        super().save(*args, **kwargs)

class Category(BaseModel):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='categories')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='children')
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True)

    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.shop.name} - Category {self.name}"
    
    def save(self, *args, **kwargs):
        # Slug Auto Create
        if not self.slug:
            self.slug = generate_unique_slug(Category,self.name,'slug')

        super().save(*args, **kwargs)

class Product(BaseModel):
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='products')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True)

    short_description = models.CharField(max_length=200)
    full_description = models.TextField()

    sku = models.CharField(max_length=100, unique=True)
    # barcode = models.CharField(max_length=50, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # compare_at_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # length × width × height  "10x5x2 cm"  
    # dimensions = models.CharField(max_length=100, blank=True, null=True)

    tags = models.CharField(max_length=255, blank=True, null=True) 

    def save(self, *args, **kwargs):
        # Slug Auto Create
        if not self.slug:
            self.slug = generate_unique_slug(Product,self.name,'slug')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.shop.name} - Product {self.name}"

    
class ProductImage(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to=PRODUCT_IMAGE_UPLOAD_TO)

    alt_text = models.CharField(max_length=200, blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

class ProductVariant(BaseModel):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variants')
    title = models.CharField(max_length=100) 
    value = models.CharField(max_length=100) 

    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return f"{self.product.name} - {self.title}: {self.value}"
