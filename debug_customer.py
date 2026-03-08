"""
Quick debug script to check customer data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mess_manager.settings')
django.setup()

from core.models import Customer

# Check all customers
customers = Customer.objects.all()
print(f"\nTotal customers: {customers.count()}\n")

for customer in customers:
    print(f"ID: {customer.customer_id}")
    print(f"Name: {customer.name}")
    print(f"Active: {customer.is_active}")
    print(f"Plan: {customer.plan_type}")
    print(f"Start: {customer.start_date}")
    print(f"End: {customer.end_date}")
    print(f"Subscription Active: {customer.is_subscription_active}")
    print("-" * 50)

# Try to find customer 5491
print("\nLooking for customer 5491:")
try:
    customer = Customer.objects.get(customer_id='5491')
    print(f"Found: {customer.name}")
    print(f"Active: {customer.is_active}")
except Customer.DoesNotExist:
    print("Customer 5491 not found!")
