from django import forms
from .models import Order


class OrderForm(forms.MobileForm):
    class Meta:
        model = Order
        fields = ('full_name','email',
                    'phone_number',
                    'street_address1','street_address2',
                    'postcode', 'county', 'country',)
    
    def __int__(self, *args, **kwargs):
        '''
        Add placehodlers and classes, remove autogen labels and set autoficus
        '''
        # First we call the default init method to set the form up as it would be by default.
        super().__int__(*args, **kwargs)

        placehodlers = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Post Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

    self.fields['full_name'].widget.attrs['autofocus'] = True

    for field in self.fields:
        if field in self.fields:
            placehodler = f'{placehodlers[field]} *'
        else:
            placehodler = {placehodlers[field]}
        self.fields[field].widget.attrs['placeholder'] = placehodler
        self.fields[field].widget.attrs['class'] = 'stripe-style-input'
        self.fields[field].labels = False
        


    