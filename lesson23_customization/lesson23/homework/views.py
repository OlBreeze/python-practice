from django.shortcuts import render
from .models import Product

def about_view(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
