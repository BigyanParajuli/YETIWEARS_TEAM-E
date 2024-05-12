from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import Userprofile, Promotion
from .forms import CustomerSignUpForm, SellerSignUpForm, UserProfileForm, PromotionForm
from store.forms import ProductForm
from store.models import Product

def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)
    promotions = user.promotions.all()
    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'products': products,
        'promotions': promotions,
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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('myaccount')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'userprofile/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']

            # Check if the old password is correct
            if not request.user.check_password(old_password):
                form.add_error('old_password', 'The old password is incorrect.')
            # Check if the new passwords match
            elif new_password1 != new_password2:
                form.add_error('new_password2', 'The new passwords do not match.')
            else:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed.')
                return redirect('myaccount')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'userprofile/change_password.html', {'form': form})

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

@login_required
def add_promotion(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.user = request.user
            promotion.save()
            messages.success(request, 'The promotion was added!')
            return redirect('my_store')
    else:
        form = PromotionForm()
    return render(request, 'userprofile/promotion_form.html', {
        'title': 'Add Promotion',
        'form': form
    })