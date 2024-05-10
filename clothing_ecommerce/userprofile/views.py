from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import Userprofile
from .forms import CustomerSignUpForm, SellerSignUpForm
from store.forms import ProductForm
from store.models import Product

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
            messages.success(request, 'The changes were saved!')
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

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.userprofile = Userprofile.objects.create(user=user)
            login(request, user)
            return redirect('frontpage')
    else:
        form = CustomerSignUpForm()
    return render(request, 'userprofile/customer_signup.html', {'form': form})

def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.userprofile = Userprofile.objects.create(user=user, is_vendor=True)
            login(request, user)
            return redirect('frontpage')
    else:
        form = SellerSignUpForm()
    return render(request, 'userprofile/seller_signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'userprofile/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        if user.userprofile.is_vendor:
            if user.userprofile.is_vendor_approved:
                messages.success(self.request, 'Welcome, seller!')
                return redirect('my_store')
            else:
                messages.warning(self.request, 'Your seller account is pending approval.')
        else:
            messages.success(self.request, 'Welcome, customer!')
        return response

@user_passes_test(lambda u: u.is_superuser)
def approve_seller(request, pk):
    userprofile = Userprofile.objects.get(pk=pk)
    userprofile.is_vendor_approved = True
    userprofile.save()
    messages.success(request, f'{userprofile.user.username} has been approved as a seller.')
    return redirect('admin:userprofile_userprofile_changelist')