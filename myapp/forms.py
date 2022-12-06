from django import forms
from myapp.models import Order, Client
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }),
        }


class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'product', 'num_units')
        labels = {
            'client': 'Client Name',
            'num_units': 'Quantity'
        }
        widgets = {
            'client': forms.RadioSelect(),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'num_units': forms.TextInput(attrs={'class': 'form-control'})
        }


class InterestForm(forms.Form):
    CHOICES = [
        ('1', 'Yes'),
        ('0', 'No')
    ]
    interested = forms.CharField(widget=forms.RadioSelect(choices=CHOICES),
                                 label='Interested')
    quantity = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter the quantity', 'class': 'form-control'}),
        required=False)
    comments = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Comments', 'class': 'form-control'}),
                               label="Additional Comments", required=False)
