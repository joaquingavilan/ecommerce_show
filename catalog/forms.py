from django import forms
from .models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all'}),
            'slug': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all', 'rows': 4}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'category', 'price', 'sizes', 'description', 'available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'}),
            'slug': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'}),
            'category': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'}),
            'price': forms.NumberInput(attrs={'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'placeholder': 'Ej: 150000'}),
            'sizes': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'placeholder': 'Ej: S, M, L'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'}),
            'available': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-primary focus:ring-primary border-gray-300 rounded cursor-pointer'}),
        }

class CheckoutForm(forms.Form):
    DELIVERY_CHOICES = [
        ('delivery', 'Delivery'),
        ('pickup', 'Retirar del Local'),
    ]
    PAYMENT_CHOICES = [
        ('transferencia', 'Transferencia Bancaria'),
        ('efectivo', 'Efectivo'),
        ('pos', 'POS / Tarjeta al Entregar'),
    ]
    
    full_name = forms.CharField(max_length=150, label="Nombre y Apellido", required=True, 
                                widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'placeholder': 'Ej: Joaquín Gavilan'}))
    phone = forms.CharField(max_length=50, label="Teléfono / WhatsApp", required=True,
                            widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'placeholder': 'Ej: +595972794582'}))
    delivery_method = forms.ChoiceField(choices=DELIVERY_CHOICES, label="Método de Entrega", required=True,
                                        widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'x-model': 'deliveryMethod'}))
    
    # Delivery only fields
    city = forms.CharField(max_length=150, label="Ciudad", required=False,
                           widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'placeholder': 'Ej: Asunción'}))
    address = forms.CharField(max_length=255, label="Dirección / Barrio", required=False,
                              widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'placeholder': 'Ej: Ri3 corrales 620 casi Pacheco'}))
    reference = forms.CharField(max_length=255, label="Referencia de la casa o fachada", required=False,
                                widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'placeholder': 'Ej: Casa grande en la esquina'}))
                                
    # Schedule
    desired_date = forms.CharField(max_length=50, label="Fecha de entrega", required=True,
                                   widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'type': 'date'}))
                                   
    TIME_RANGE_CHOICES = [
        ('11 a 15', 'De 11:00 a 15:00'),
        ('15 a 18', 'De 15:00 a 18:00'),
        ('18 a 22', 'De 18:00 a 22:00'),
        ('Lo antes posible', 'Lo antes posible')
    ]
    time_range = forms.ChoiceField(choices=TIME_RANGE_CHOICES, label="Rango de horario de entrega", required=True,
                                 widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'}))

    # Billing
    needs_invoice = forms.BooleanField(label="¿Desea Factura?", required=False, 
                                       widget=forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded cursor-pointer', 'x-model': 'needsInvoice'}))
    business_name = forms.CharField(max_length=150, label="Razón Social", required=False,
                                    widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'}))
    ruc = forms.CharField(max_length=50, label="RUC", required=False,
                          widget=forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'}))
    invoice_email = forms.EmailField(label="Correo electrónico (Opcional)", required=False,
                                     widget=forms.EmailInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm', 'placeholder': 'Ej: joaquinrgavilan@gmail.com'}))
                                     
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, label="Método de Pago", required=True,
                                       widget=forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-emerald-500 focus:ring-emerald-500 sm:text-sm'}))
                                       
    def clean(self):
        cleaned_data = super().clean()
        delivery = cleaned_data.get('delivery_method')
        address = cleaned_data.get('address')
        
        needs_invoice = cleaned_data.get('needs_invoice')
        business_name = cleaned_data.get('business_name')
        ruc = cleaned_data.get('ruc')
        
        if delivery == 'delivery' and not address:
            self.add_error('address', 'La dirección es requerida para el servicio de Delivery.')
            
        if needs_invoice:
            if not business_name:
                self.add_error('business_name', 'La Razón Social es requerida para la factura.')
            if not ruc:
                self.add_error('ruc', 'El RUC es requerido para la factura.')
                
        return cleaned_data
