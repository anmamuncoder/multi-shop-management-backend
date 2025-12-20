from django.contrib import admin

# Register your models here.
from .models import Wireframe,Testimonial,FAQ,Feature

@admin.register(Wireframe)
class WireframeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'website_link', 'created_at', 'updated_at')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'designation', 'ratting', 'created_at', 'updated_at')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'created_at', 'updated_at')
    
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'created_at', 'updated_at')

