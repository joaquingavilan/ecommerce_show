from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(help_text="Precio en Guaraníes (sin decimales)")
    sizes = models.CharField(max_length=255, blank=True, help_text='Tallas o medidas disponibles, separadas por coma. Ej: S, M, L o 38, 40, 42')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    @property
    def image_url(self):
        main_image = self.images.filter(is_main=True).first()
        if not main_image:
            main_image = self.images.first()
            
        if main_image and main_image.image:
            return main_image.image.url
        return ''
        
    def get_sizes_list(self):
        if not self.sizes:
            return []
        return [s.strip() for s in self.sizes.split(',') if s.strip()]

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen para {self.product.title}"
        
    class Meta:
        ordering = ['-is_main', '-created_at']

class Cart(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for session {self.session_key}"
        
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        size_str = f" (Talla: {self.size})" if self.size else ""
        return f"{self.quantity} of {self.product.title}{size_str}"
        
    @property
    def total_price(self):
        return self.product.price * self.quantity
