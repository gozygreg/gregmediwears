from django import forms
from .models import ShippingAddress, Order


class ShippingForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = ShippingAddress
        fields = ('full_name', 'email', 'address1', 'address2',
                  'town_or_city', 'county', 'postcode', 'country')
        exclude = ['user',]

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'address1': 'Address 1',
            'address2': 'Address 2',
            'town_or_city': 'Town or City',
            'postcode': 'Post code',
            'county': 'County',
            'country': 'Country'
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
