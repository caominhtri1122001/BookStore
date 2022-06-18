from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    Name = forms.CharField(label='Name',
                           required=False,
                           widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Enter the name'
                           }))

    Price = forms.CharField(label='Price',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control'
                            }))
    Image = forms.ImageField(label='Image',)

    class Meta:
        model = Book
        fields = [
            # 'name',
            # 'price',
            # # 'digital',
            # 'image',
        ]
