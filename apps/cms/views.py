from django.shortcuts import render

# Create your views here. 
from .models import Wireframe,Testimonial,FAQ,Feature

def home(request):
    wireframe = Wireframe.objects.first()
    testimonials = Testimonial.objects.all()
    faqs = FAQ.objects.all()
    features = Feature.objects.all()
    context = {
        'wireframe': wireframe,
        'testimonials': testimonials,
        'faqs': faqs,
        'features_1': features[0],
        'features_2': features[1],
        'features_3': features[2],
    }
    
    return render(request,template_name='home.html',context=context)