from django import forms
from .models import Customer, Attendance
from django.utils import timezone


class CustomerIDForm(forms.Form):
    """Form for customer ID entry"""
    customer_id = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 text-2xl text-center font-bold border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none',
            'placeholder': '0000',
            'pattern': '[0-9]{4}',
            'inputmode': 'numeric',
            'autofocus': True,
        }),
        label='Enter Your 4-Digit ID'
    )
    
    def clean_customer_id(self):
        customer_id = self.cleaned_data.get('customer_id')
        if not customer_id.isdigit():
            raise forms.ValidationError('ID must contain only numbers.')
        if not Customer.objects.filter(customer_id=customer_id, is_active=True).exists():
            raise forms.ValidationError('Invalid ID or subscription inactive.')
        return customer_id


class AttendanceForm(forms.ModelForm):
    """Form for marking attendance"""
    
    class Meta:
        model = Attendance
        fields = ['meal_type']
        widgets = {
            'meal_type': forms.HiddenInput()
        }


class CustomerForm(forms.ModelForm):
    """Form for creating/editing customers"""
    
    class Meta:
        model = Customer
        fields = [
            'name', 'phone_number', 'plan_type',
            'start_date', 'end_date', 'lunch_time', 'dinner_time', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Customer Name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '+919876543210'
            }),
            'plan_type': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'lunch_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'dinner_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('End date must be after start date.')
        
        return cleaned_data
