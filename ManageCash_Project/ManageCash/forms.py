
from django import forms
from ManageCash.models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

#Registration(username, email, password, confirm password) pages.

class RegisterForm(UserCreationForm):
    class Meta:
        model=UserModel
        fields=['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    pass

class CashForm(forms.ModelForm):
    class Meta:
        model=CashModel
        fields='__all__'
        exclude=['user']
        
        widgets = {
        'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class ExpenseForm(forms.ModelForm):
    class Meta:
        model=ExpenseModel
        fields='__all__'
        exclude=['user']
        
        widgets = {
        'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }