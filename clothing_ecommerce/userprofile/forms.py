from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Promotion

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SellerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
from django import forms
from django.contrib.auth.models import User
from .models import Userprofile

class UserProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs['instance']
        if user:
            # Get UserProfile instance
            profile = user.userprofile
            initial = kwargs.get('initial', {})
            initial['phone'] = profile.phone
            initial['address'] = profile.address
            kwargs['initial'] = initial

        super(UserProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        if commit:
            user.save()
            user_profile = user.userprofile
            user_profile.phone = self.cleaned_data['phone']
            user_profile.address = self.cleaned_data['address']
            user_profile.save()
        return user

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['product', 'discount_percentage', 'start_date', 'end_date']