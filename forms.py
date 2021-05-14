from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

from .models import *

class EmpForm(ModelForm):
    class Meta:
        model = Emp
        fields = '__all__'
        exclude = ['user']

class PatientListForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']


class AppointmentForm(ModelForm):
    class Meta:
        model= Appointment
        fields = '__all__'

