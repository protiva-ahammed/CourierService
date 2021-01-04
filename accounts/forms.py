
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from .models import Order
from .models import Customer
from .models import GeneralOrder


class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class GeneralOrderForm(ModelForm):
    class Meta:
        model = GeneralOrder
        fields=['customer_name','contract','address','email','description','payment','status','receiver','phn','destination','packing']#fields = '__all__'