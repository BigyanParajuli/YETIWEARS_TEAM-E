from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import Userprofile
from .forms import SignUpForm  # Import the custom SignUpForm
from store.forms import ProductForm
from store.models import Product
from django.shortcuts import render
from .models import Product

def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'products': products,
    })

@login_required
def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)
    return render(request, 'userprofile/my_store.html', {
        'products': products
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()
            messages.success(request, 'The product was added!')
            return redirect('my_store')
    else:
        form = ProductForm()
    return render(request, 'userprofile/product_form.html', {
        'title': 'Add product',
        'form': form
    })

@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'The changes was saved!')
            return redirect('my_store')
    else:
        form = ProductForm(instance=product)
    return render(request, 'userprofile/product_form.html', {
        'title': 'Edit product',
        'product': product,
        'form': form
    })

@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()
    messages.success(request, 'The product was deleted!')
    return redirect('my_store')

@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Use the custom SignUpForm
        if form.is_valid():
            user = form.save()
            user.userprofile = Userprofile.objects.create(user=user)  # Create Userprofile instance
            login(request, user)
            return redirect('frontpage')
    else:
        form = SignUpForm()  # Use the custom SignUpForm
    return render(request, 'userprofile/signup.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/product_list.html', context)

def my_store(request):
    products = request.user.products.exclude(status=Product.DELETED)

def my_store(request):
    return render(request, 'userprofile/my_store.html')