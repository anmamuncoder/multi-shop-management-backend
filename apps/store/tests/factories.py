import factory
# Internal
from ..models import Shop,Category,Product,ProductImage,ProductVariant
# Enternal
from apps.accounts.models import User
from apps.accounts.tests.factories import UserFactory

# --------------------------------
# Shop Factory Object Create
# --------------------------------
class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda o : f"User {o}")
    description = factory.Sequence(lambda o : f"description {o}")
    short_intro = factory.Sequence(lambda o : f"short_intro {o}")
    policies = factory.Sequence(lambda o : f"policies {o}")
    currency = factory.Iterator(['BDT','USD','EUR','INR'])
    tax_rate = 10.0

# --------------------------------
# Shop Factory Object Create
# --------------------------------
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    shop = factory.SubFactory(ShopFactory)
    name = factory.Sequence(lambda o : f"User {o}")
    
# --------------------------------
# Shop Factory Object Create
# --------------------------------
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    shop = factory.SubFactory(ShopFactory)
    category = factory.SubFactory(CategoryFactory)

    name = factory.Sequence(lambda o : f"User {o}")
    short_description = factory.Sequence(lambda o : f"short_description {o}")
    full_description = factory.Sequence(lambda o : f"full_description {o}")

    sku = factory.Sequence(lambda o : f"SKU-{o}")

# --------------------------------
# Shop Factory Object Create
# --------------------------------
class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage
    product = factory.SubFactory(ProductFactory) 
    alt_text = factory.Sequence(lambda o : f"IMAGE-{o}")

# --------------------------------
# Shop Factory Object Create
# --------------------------------
class ProductVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariant
    product = factory.SubFactory(ProductFactory)
    title = factory.Sequence(lambda o : f"title-{o}")
    value = factory.Sequence(lambda o : f"value-{o}")

    sku = factory.Sequence(lambda o : f"SKU-VARIANT-{o}")
    
