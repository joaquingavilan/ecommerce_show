from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

staff_member_required = user_passes_test(lambda u: u.is_active and u.is_staff)
from .models import Product, Category, ProductImage
from .forms import CategoryForm, ProductForm

@staff_member_required
def dashboard_home(request):
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    recent_products = Product.objects.order_by('-created')[:5]
    
    context = {
        'product_count': product_count,
        'category_count': category_count,
        'recent_products': recent_products,
    }
    return render(request, 'catalog/dashboard/home.html', context)

@staff_member_required
def manage_products(request):
    products = Product.objects.all().order_by('-created')
    return render(request, 'catalog/dashboard/products.html', {'products': products})

@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'catalog/dashboard/categories.html', {'categories': categories})

# --- HTMX Category CRUD ---

@staff_member_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'categoryListChanged'})
    else:
        form = CategoryForm()
    
    return render(request, 'catalog/dashboard/partials/category_form.html', {'form': form, 'title': 'Nueva Categoría'})

@staff_member_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'categoryListChanged'})
    else:
        form = CategoryForm(instance=category)
        
    return render(request, 'catalog/dashboard/partials/category_form.html', {'form': form, 'category': category, 'title': 'Editar Categoría'})

@staff_member_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return HttpResponse(status=204, headers={'HX-Trigger': 'categoryListChanged'})
        
    return render(request, 'catalog/dashboard/partials/category_delete_confirm.html', {'category': category})

@staff_member_required
def category_list_partial(request):
    categories = Category.objects.all()
    return render(request, 'catalog/dashboard/partials/category_list_content.html', {'categories': categories})

# --- HTMX Product CRUD ---

@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            for i, image_file in enumerate(request.FILES.getlist('images')):
                ProductImage.objects.create(product=product, image=image_file, is_main=(i == 0))
            return HttpResponse(status=204, headers={'HX-Trigger': 'productListChanged'})
    else:
        form = ProductForm()
    
    return render(request, 'catalog/dashboard/partials/product_form.html', {'form': form, 'title': 'Nuevo Producto'})

@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            new_images = request.FILES.getlist('images')
            if new_images:
                has_main = product.images.filter(is_main=True).exists()
                for i, image_file in enumerate(new_images):
                    is_main = not has_main and (i == 0)
                    ProductImage.objects.create(product=product, image=image_file, is_main=is_main)
            return HttpResponse(status=204, headers={'HX-Trigger': 'productListChanged'})
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'catalog/dashboard/partials/product_form.html', {'form': form, 'product': product, 'title': 'Editar Producto'})

@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return HttpResponse(status=204, headers={'HX-Trigger': 'productListChanged'})
        
    return render(request, 'catalog/dashboard/partials/product_delete_confirm.html', {'product': product})

@staff_member_required
def product_image_delete(request, pk):
    image = get_object_or_404(ProductImage, pk=pk)
    product = image.product
    if request.method == 'POST':
        was_main = image.is_main
        image.delete()
        if was_main:
            first_img = product.images.first()
            if first_img:
                first_img.is_main = True
                first_img.save()
        response = render(request, 'catalog/dashboard/partials/product_image_gallery.html', {'product': product})
        response['HX-Trigger'] = 'productListChanged'
        return response
    return HttpResponse(status=400)

@staff_member_required
def product_image_main(request, pk):
    image = get_object_or_404(ProductImage, pk=pk)
    product = image.product
    if request.method == 'POST':
        product.images.update(is_main=False)
        image.is_main = True
        image.save()
        response = render(request, 'catalog/dashboard/partials/product_image_gallery.html', {'product': product})
        response['HX-Trigger'] = 'productListChanged'
        return response
    return HttpResponse(status=400)

@staff_member_required
def product_list_partial(request):
    products = Product.objects.all().order_by('-created')
    return render(request, 'catalog/dashboard/partials/product_list_content.html', {'products': products})
