from django import forms
from .models import Product

def validate_not_zero(value):
    if value == 0:
        raise forms.ValidationError("Цена не может быть нулевой!")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'})
        }

    price = forms.DecimalField(validators=[validate_not_zero])
