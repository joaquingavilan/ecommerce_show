from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem
from .forms import CheckoutForm
import urllib.parse

@require_POST
def demo_auto_login(request):
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    
    if user:
        login(request, user)
        return redirect('dashboard_home')
    return redirect('store_front')

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def store_front(request):
    categories = Category.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug, available=True)
    else:
        products = Product.objects.filter(available=True)
        
    cart = get_or_create_cart(request)
    cart_count = sum(item.quantity for item in cart.items.all())

    context = {
        'categories': categories,
        'products': products,
        'cart_count': cart_count,
        'current_category': category_slug
    }
    
    # If the request is from HTMX, return just the product list partial
    if request.htmx:
        return render(request, 'catalog/partials/product_list.html', context)
        
    return render(request, 'catalog/store.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart = get_or_create_cart(request)
    cart_count = sum(item.quantity for item in cart.items.all())
    
    context = {
        'product': product,
        'cart_count': cart_count,
    }
    return render(request, 'catalog/product_detail.html', context)

@require_POST
def add_to_cart(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    size = request.POST.get('size', '')
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    cart_count = sum(item.quantity for item in cart.items.all())
    
    # Return simply the updated cart count for the icon
    context = {'cart_count': cart_count, 'added': True, 'product': product}
    return render(request, 'catalog/partials/cart_count.html', context)


def view_cart(request):
    cart = get_or_create_cart(request)
    context = {'cart': cart}
    return render(request, 'catalog/cart.html', context)
    

@require_POST
def update_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    action = request.POST.get('action')
    if action == 'increment':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            
    # HTMX request returning the updated cart partial
    context = {'cart': cart}
    return render(request, 'catalog/partials/cart_details.html', context)

@require_POST
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    # HTMX request returning the updated cart partial
    context = {'cart': cart}
    return render(request, 'catalog/partials/cart_details.html', context)


def checkout_view(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect('store_front')
        
    form = CheckoutForm()
    context = {'cart': cart, 'form': form}
    return render(request, 'catalog/checkout.html', context)

@require_POST
def checkout_whatsapp(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        return redirect('store_front')
        
    form = CheckoutForm(request.POST)
    
    if not form.is_valid():
        context = {'cart': cart, 'form': form}
        return render(request, 'catalog/checkout.html', context)
        
    # Cleaned data
    cd = form.cleaned_data
    
    # 1. Header
    delivery_str = "delivery" if cd['delivery_method'] == 'delivery' else "retirar del local"
    message = f"Hola 👋, mi nombre es {cd['full_name']}, y me gustaría realizar un pedido para {delivery_str}!\n\n"
    
    # 2. Schedule
    message += f"Fecha que deseo el pedido: {cd['desired_date']}\n"
    message += f"Rango de Horario de Entrega: {cd['time_range']}\n\n\n"
    
    # 3. Product Details
    message += "Mi Pedido es:\n\n"
    for item in cart.items.all():
        message += f"- {item.product.title}\n"
        message += f"- Cantidad: {item.quantity}\n"
        if item.size:
             message += f"- Medida: {item.size}\n"
        message += f"- SubTotal: Gs. {intcomma(item.total_price)}\n\n"
        
    message += "\n - - - - - - - - - - - - - - - - - - - - - -\n\n"
    
    # 4. Customer Data
    message += "Mis datos son:\n\n"
    message += f"- {cd['full_name']}\n"
    message += f"- {cd['phone']}\n"
    
    if cd['delivery_method'] == 'delivery':
        if cd['city']:
            message += f"- Ciudad: {cd['city']}\n"
        message += f"- Dirección: {cd['address']}\n"
        if cd['reference']:
            message += f"- Ref: {cd['reference']}\n"
            
    if cd['needs_invoice']:
        message += f"- Quiero Factura ({cd['business_name']} / {cd['ruc']})\n"
        if cd['invoice_email']:
            message += f"- Email para Enviar Factura: {cd['invoice_email']}\n"
    else:
        message += "- Sin Factura\n"
        
    payment_method_display = dict(CheckoutForm.PAYMENT_CHOICES).get(cd['payment_method'], cd['payment_method'].replace('_', ' ').title())
    message += f"- Metodo de pago: {payment_method_display.split(' ')[0] if cd['payment_method'] == 'transferencia' else payment_method_display}\n"
    message += f"- Total: Gs. {intcomma(cart.total_price)}\n"

    encoded_message = urllib.parse.quote(message)
    # Target phone number
    whatsapp_url = f"https://wa.me/595972794582?text={encoded_message}"
    
    return HttpResponseRedirect(whatsapp_url)
