"""
Debug timezone issue
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mess_manager.settings')
django.setup()

from django.utils import timezone
from core.models import Customer

customer = Customer.objects.get(customer_id='5491')
today = timezone.now().date()

print(f"\nCustomer: {customer.name}")
print(f"Start Date: {customer.start_date} (type: {type(customer.start_date)})")
print(f"End Date: {customer.end_date} (type: {type(customer.end_date)})")
print(f"Today: {today} (type: {type(today)})")
print(f"\nComparisons:")
print(f"start_date <= today: {customer.start_date <= today}")
print(f"today <= end_date: {today <= customer.end_date}")
print(f"is_active: {customer.is_active}")
print(f"\nFull check: {customer.is_active and customer.start_date <= today <= customer.end_date}")
