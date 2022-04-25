from django import forms
from django.forms import ModelForm, TextInput, Select
from django_select2.forms import ModelSelect2Widget

from .models import *
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']


class LobbyForm(ModelForm):
    class Meta:
        model = Lobby
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'name', 'bio']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_contactnumber', 'customer_address', 'quantity', 'total_price']


class ProductForm(ModelForm):
    product_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Product Name'}))
    product_details = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter Product Details'}))
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_by', 'created_date']


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(ModelForm):
    task_details = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter Task Details'}))
    remarks = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter Remarks'}))

    class Meta:
        model = Tasks
        fields = '__all__'
        exclude = ['created_by', 'created_date', 'assign_date', 'assigned_to', 'completed_by']
        widgets = {
            'deadline_date': DateInput(),
        }
