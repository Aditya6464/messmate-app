from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import random


class Customer(models.Model):
    """Customer model for mess subscribers"""
    
    PLAN_CHOICES = [
        ('LUNCH_ONLY', 'Lunch Only'),
        ('DINNER_ONLY', 'Dinner Only'),
        ('BOTH', 'Both (Lunch + Dinner)'),
    ]
    
    customer_id = models.CharField(
        max_length=4,
        unique=True,
        editable=False,
        help_text="Auto-generated 4-digit unique ID"
    )
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    plan_type = models.CharField(max_length=15, choices=PLAN_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    lunch_time = models.TimeField(help_text="Preferred lunch time")
    dinner_time = models.TimeField(help_text="Preferred dinner time")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer_id']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.customer_id} - {self.name}"
    
    def save(self, *args, **kwargs):
        """Generate unique 4-digit customer ID if not exists"""
        if not self.customer_id:
            self.customer_id = self.generate_unique_id()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_unique_id():
        """Generate a unique 4-digit ID"""
        while True:
            new_id = str(random.randint(1000, 9999))
            if not Customer.objects.filter(customer_id=new_id).exists():
                return new_id
    
    @property
    def is_subscription_active(self):
        """Check if subscription is currently active"""
        today = timezone.localtime(timezone.now()).date()
        return self.is_active and self.start_date <= today <= self.end_date
    
    @property
    def days_remaining(self):
        """Calculate days remaining in subscription"""
        if not self.is_subscription_active:
            return 0
        today = timezone.localtime(timezone.now()).date()
        return (self.end_date - today).days

    @property
    def is_expiring_soon(self):
        """Check if subscription expires in 2 days"""
        return self.days_remaining <= 2 and self.days_remaining > 0
    
    def can_mark_lunch(self):
        """Check if customer can mark lunch attendance"""
        return self.plan_type in ['LUNCH_ONLY', 'BOTH']
    
    def can_mark_dinner(self):
        """Check if customer can mark dinner attendance"""
        return self.plan_type in ['DINNER_ONLY', 'BOTH']


class Attendance(models.Model):
    """Attendance tracking for meals"""
    
    MEAL_CHOICES = [
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
    ]
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    date = models.DateField(default=timezone.now)
    meal_type = models.CharField(max_length=10, choices=MEAL_CHOICES)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-marked_at']
        unique_together = ['customer', 'date', 'meal_type']
        indexes = [
            models.Index(fields=['date', 'meal_type']),
            models.Index(fields=['customer', 'date']),
        ]
    
    def __str__(self):
        return f"{self.customer.customer_id} - {self.meal_type} - {self.date}"
    
    @classmethod
    def get_today_count(cls, meal_type=None):
        """Get today's attendance count"""
        today = timezone.localtime(timezone.now()).date()
        queryset = cls.objects.filter(date=today)
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)
        return queryset.count()
    
    @classmethod
    def has_marked_today(cls, customer, meal_type):
        """Check if customer has already marked attendance for today"""
        today = timezone.localtime(timezone.now()).date()
        return cls.objects.filter(
            customer=customer,
            date=today,
            meal_type=meal_type
        ).exists()
