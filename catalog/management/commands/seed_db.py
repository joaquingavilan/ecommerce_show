from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds the database with initial categories and products'

    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Create Categories
        cat_electronics = Category.objects.create(name='Electrónica', slug='electronica', description='Última tecnología y gadgets.')
        cat_clothing = Category.objects.create(name='Ropa', slug='ropa', description='Ropa para todas las ocasiones.')
        cat_home = Category.objects.create(name='Hogar & Jardín', slug='hogar-jardin', description='Todo para tu casa.')
        cat_sports = Category.objects.create(name='Deportes', slug='deportes', description='Equipamiento deportivo.')

        # Create Products
        products_data = [
            {
                'category': cat_electronics,
                'title': 'Auriculares Inalámbricos Pro',
                'slug': 'auriculares-pro',
                'description': 'Auriculares Bluetooth con cancelación de ruido activa.',
                'price': 129.99,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=800&auto=format&fit=crop',
            },
            {
                'category': cat_electronics,
                'title': 'Reloj Inteligente Serie 5',
                'slug': 'reloj-inteligente-5',
                'description': 'Monitoriza tu ritmo cardíaco, pasos, y rutinas de ejercicio diarias.',
                'price': 199.50,
                'image_url': 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?q=80&w=800&auto=format&fit=crop',
            },
            {
                'category': cat_clothing,
                'title': 'Camiseta de Algodón Básica',
                'slug': 'camiseta-algodon',
                'description': 'Camiseta 100% algodón, diseño minimalista.',
                'price': 19.99,
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=800&auto=format&fit=crop',
            },
            {
                'category': cat_home,
                'title': 'Cafetera Espresso Manual',
                'slug': 'cafetera-espresso',
                'description': 'Disfruta de café nivel barista desde la comodidad de tu casa.',
                'price': 89.00,
                'image_url': 'https://images.unsplash.com/photo-1520262454473-a1a82276a574?q=80&w=800&auto=format&fit=crop',
            },
            {
                'category': cat_sports,
                'title': 'Esterilla de Yoga Premium',
                'slug': 'esterilla-yoga',
                'description': 'Material antideslizante y ecológico para tus rutinas.',
                'price': 34.50,
                'image_url': 'https://images.unsplash.com/photo-1592432608018-94446bfb7724?q=80&w=800&auto=format&fit=crop',
            },
            {
                'category': cat_clothing,
                'title': 'Zapatillas Deportivas Urbanas',
                'slug': 'zapatillas-urbanas',
                'description': 'Zapatillas ligeras, cómodas y transpirables para uso diario.',
                'price': 59.99,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=800&auto=format&fit=crop',
            }
        ]

        for p_data in products_data:
            Product.objects.create(**p_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))
