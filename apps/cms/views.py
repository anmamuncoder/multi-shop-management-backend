from django.shortcuts import render

# Create your views here. 
from .models import Wireframe,Testimonial,FAQ,Feature

def home(request):
    wireframe = Wireframe.objects.first()
    testimonials = Testimonial.objects.all()
    faqs = FAQ.objects.all()
    features = Feature.objects.all().order_by('price')[:3]
    context = {
        'wireframe': wireframe,
        'testimonials': testimonials,
        'faqs': faqs,
        'features': features,
    }

    return render(request,template_name='home.html',context=context)