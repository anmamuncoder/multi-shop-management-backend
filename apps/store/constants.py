CURRENCY_CHOICES = [
    ('BDT', 'Bangladeshi Taka'),
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('INR', 'Indian Rupee'),
]

 
def PRODUCT_IMAGE_UPLOAD_TO(instance, filename):
    """
    media/product/<product-slug>/<filename>
    """
    return f'product/{instance.product.slug}/{filename}'
