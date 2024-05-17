import stripe
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from .forms import OrderForm
from .models import Category, Product, Order, OrderItem

def frontpage(request):
    latest_products = Product.objects.filter(status=Product.ACTIVE).order_by('-created_at')[:3]
    products = Product.objects.filter(status=Product.ACTIVE)[3:]
    cart = Cart(request)

    return render(request, 'core/frontpage.html', {
        'latest_products': latest_products,
        'products': products,
        'cart': cart,
    })

def about(request):
    return render(request, 'core/about.html')

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('cart_view')

def success(request):
    return render(request, 'store/success.html')

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

    if cart.get_total_cost() == 0:
        return redirect('cart_view')

    if request.method == 'POST':
        data = json.loads(request.body)
        form = OrderForm(request.POST)

        total_price = int(cart.get_total_cost() + 100)  # Round the total cost to the nearest integer

        items = []
        for item in cart:
            product = item['product']
            items.append({
                'price_data': {
                    'currency': 'npr',
                    'product_data': {
                        'name': product.title,
                    },
                    'unit_amount': int(product.price * 100),  # Convert the price to an integer
                },
                'quantity': item['quantity']
            })

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url=f'{settings.WEBSITE_URL}cart/success/',
            cancel_url=f'{settings.WEBSITE_URL}cart/',
        )
        payment_intent = session.payment_intent

        order = Order.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            zipcode=data['zipcode'],
            city=data['city'],
            created_by=request.user,
            is_paid=True,
            payment_intent=payment_intent,
            paid_amount=total_price
        )

        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity

            item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

        cart.clear()

        return JsonResponse({'session': session, 'order': payment_intent})
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
        'pub_key': settings.STRIPE_PUBLIC_KEY,
    })

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'store/search.html', {
        'query': query,
        'products': products,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)

    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
    cart = Cart(request)
    return render(request, 'store/product_detail.html', {'product': product, 'similar_products': similar_products, 'cart': cart})