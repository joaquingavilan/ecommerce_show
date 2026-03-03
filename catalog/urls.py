from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import admin_views

urlpatterns = [
    # Storefront
    path('', views.store_front, name='store_front'),
    path('demo-login/', views.demo_auto_login, name='demo_auto_login'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('checkout/whatsapp/', views.checkout_whatsapp, name='checkout_whatsapp'),
    
    # Custom Admin Dashboard Auth
    path('dashboard/login/', auth_views.LoginView.as_view(template_name='catalog/dashboard/login.html', redirect_authenticated_user=True), name='dashboard_login'),
    path('dashboard/logout/', auth_views.LogoutView.as_view(next_page='store_front'), name='dashboard_logout'),

    # Custom Admin Dashboard
    path('dashboard/', admin_views.dashboard_home, name='dashboard_home'),
    path('dashboard/products/', admin_views.manage_products, name='manage_products'),
    path('dashboard/categories/', admin_views.manage_categories, name='manage_categories'),
    
    # HTMX Admin Endpoints (Categories)
    path('dashboard/categories/list/', admin_views.category_list_partial, name='category_list_partial'),
    path('dashboard/categories/create/', admin_views.category_create, name='category_create'),
    path('dashboard/categories/<int:pk>/edit/', admin_views.category_edit, name='category_edit'),
    path('dashboard/categories/<int:pk>/delete/', admin_views.category_delete, name='category_delete'),

    # HTMX Admin Endpoints (Products)
    path('dashboard/products/list/', admin_views.product_list_partial, name='product_list_partial'),
    path('dashboard/products/create/', admin_views.product_create, name='product_create'),
    path('dashboard/products/<int:pk>/edit/', admin_views.product_edit, name='product_edit'),
    path('dashboard/products/<int:pk>/delete/', admin_views.product_delete, name='product_delete'),
    
    # HTMX Admin Endpoints (Product Images)
    path('dashboard/images/<int:pk>/delete/', admin_views.product_image_delete, name='product_image_delete'),
    path('dashboard/images/<int:pk>/main/', admin_views.product_image_main, name='product_image_main'),
]
