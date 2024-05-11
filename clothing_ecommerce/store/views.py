from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from .forms import OrderForm
from .models import Category, Product, Order, OrderItem

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

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart_view')

def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    if action:
        quantity = 1
        if action == 'decrease':
            quantity = -1
        cart = Cart(request)
        cart.add(product_id, quantity, True)
    return redirect('cart_view')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'store/cart_view.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total_price = 0
            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])
            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()
            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity
                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            cart.clear()
            return redirect('myaccount')
    else:
        form = OrderForm()
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))
    cart = Cart(request)  # Create a Cart instance
    return render(request, 'store/search.html', {'query': query, 'products': products, 'cart': cart})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    cart = Cart(request)  # Create a Cart instance
    return render(request, 'store/category_detail.html', {'category': category, 'products': products, 'cart': cart})

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    cart = Cart(request)  # Create a Cart instance
    return render(request, 'store/product_detail.html', {'product': product, 'cart': cart})

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
    cart = Cart(request)
    return render(request, 'store/product_detail.html', {'product': product, 'similar_products': similar_products, 'cart': cart})