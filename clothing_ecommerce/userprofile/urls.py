from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('signup/customer/', views.customer_signup, name='customer_signup'),
    path('signup/seller/', views.seller_signup, name='seller_signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('my-store/', views.my_store, name='my_store'),
    path('my-store/order-detail/<int:pk>/', views.my_store_order_detail, name='my_store_order_detail'),
    path('my-store/add-product/', views.add_product, name='add_product'),
    path('my-store/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my-store/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('my-store/add-promotion/', views.add_promotion, name='add_promotion'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('approve-seller/<int:pk>/', views.approve_seller, name='approve_seller'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]