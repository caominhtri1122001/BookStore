from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    name = forms.CharField(label='Name',
                           required=False,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Enter the name'
                           }))

    price = forms.CharField(label='Price',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control'
                            }))
    image = forms.ImageField(label='Image', required=False)

    class Meta:
        model = Book
        fields = [
            'name',
            'price',
            # 'digital',
            'image',
            'category'
        ]
