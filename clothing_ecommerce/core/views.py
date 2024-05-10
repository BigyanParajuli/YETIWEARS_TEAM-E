from django.shortcuts import render

from store.cart import Cart
from store.models import Product

def frontpage(request):
    latest_products = Product.objects.filter(status=Product.ACTIVE).order_by('-created_at')[:3]
    products = Product.objects.filter(status=Product.ACTIVE)[3:]
    cart = Cart(request)  # Create a Cart instance

    return render(request, 'core/frontpage.html', {
        'latest_products': latest_products,
        'products': products,
        'cart': cart,  # Pass the cart instance to the template
    })

def about(request):
    return render(request, 'core/about.html')


