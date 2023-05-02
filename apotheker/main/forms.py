from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Drug, Receipt, ReceiptSchedule


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'description']


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['drug', 'start_dt', 'days']


class ReceiptScheduleForm(forms.ModelForm):
    class Meta:
        model = ReceiptSchedule
        fields = ['time', 'amount', 'receipt']


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
