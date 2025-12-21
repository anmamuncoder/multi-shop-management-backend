from django.db import models

# Create your models here.
from apps.base.models import BaseModel

class Wireframe(BaseModel):
    logo = models.ImageField(upload_to='cms/wireframes/logos/', null=True, blank=True)
    facebook_link = models.URLField(max_length=255, null=True, blank=True)
    twitter_link = models.URLField(max_length=255, null=True, blank=True)
    instagram_link = models.URLField(max_length=255, null=True, blank=True)
    linkedin_link = models.URLField(max_length=255, null=True, blank=True)
    website_link = models.URLField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Wireframe"
        verbose_name_plural = "Wireframes"

    def __str__(self):
        return f"Wireframe {self.id}"
        
    
class Testimonial(BaseModel):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    feedback = models.TextField()
    ratting = models.IntegerField(default=0,help_text="Ratting out of 5")
    photo = models.ImageField(upload_to='cms/testimonials/photos/', null=True, blank=True)

    def __str__(self):
        return f"Testimonial by {self.name}"

class FAQ(BaseModel):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return f"FAQ: {self.question}"


class Feature(BaseModel):
    title = models.CharField(max_length=255,help_text="Feature Title")
    price = models.DecimalField(max_digits=10, decimal_places=2,help_text="Feature Price")
    description = models.TextField(help_text="Feature Description write saparately with comma") 

    def __str__(self):
        return f"Feature: {self.title}"

