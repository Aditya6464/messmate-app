from django.contrib import admin
from .models import Customer, Attendance


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'name', 'phone_number', 'plan_type', 'start_date', 'end_date', 'is_active']
    list_filter = ['plan_type', 'is_active', 'created_at']
    search_fields = ['customer_id', 'name', 'phone_number']
    readonly_fields = ['customer_id', 'created_at', 'updated_at']
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_id', 'name', 'phone_number')
        }),
        ('Subscription Details', {
            'fields': ('plan_type', 'start_date', 'end_date', 'lunch_time', 'dinner_time', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date', 'meal_type', 'marked_at']
    list_filter = ['meal_type', 'date']
    search_fields = ['customer__customer_id', 'customer__name']
    date_hierarchy = 'date'
    readonly_fields = ['marked_at']
