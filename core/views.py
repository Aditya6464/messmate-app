"""
Customer-facing views for attendance marking
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, time
from .models import Customer, Attendance
from .forms import CustomerIDForm, AttendanceForm
from django.conf import settings


class CustomerIDEntryView(View):
    """View for customer ID entry"""
    
    def get(self, request):
        form = CustomerIDForm()
        return render(request, 'customer/id_entry.html', {'form': form})
    
    def post(self, request):
        form = CustomerIDForm(request.POST)
        if form.is_valid():
            customer_id = form.cleaned_data['customer_id']
            return redirect('mark_attendance', customer_id=customer_id)
        return render(request, 'customer/id_entry.html', {'form': form})


class MarkAttendanceView(View):
    """View for marking attendance"""
    
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, customer_id=customer_id, is_active=True)
        
        # Check if subscription is active
        if not customer.is_subscription_active:
            messages.error(request, 'Your subscription has expired. Please renew to continue.')
            return redirect('customer_id_entry')
        
        # Check which meals can be marked
        today = timezone.localtime(timezone.now()).date()
        context = {
            'customer': customer,
            'can_mark_lunch': customer.can_mark_lunch(),
            'can_mark_dinner': customer.can_mark_dinner(),
            'lunch_already_marked': Attendance.has_marked_today(customer, 'LUNCH'),
            'dinner_already_marked': Attendance.has_marked_today(customer, 'DINNER'),
            'is_lunch_time': self.is_within_time_window('lunch'),
            'is_dinner_time': self.is_within_time_window('dinner'),
            'today': today,
        }
        
        return render(request, 'customer/mark_attendance.html', context)
    
    def post(self, request, customer_id):
        customer = get_object_or_404(Customer, customer_id=customer_id, is_active=True)
        meal_type = request.POST.get('meal_type')
        
        # Validate meal type
        if meal_type not in ['LUNCH', 'DINNER']:
            messages.error(request, 'Invalid meal type.')
            return redirect('mark_attendance', customer_id=customer_id)
        
        # Check if customer can mark this meal
        if meal_type == 'LUNCH' and not customer.can_mark_lunch():
            messages.error(request, 'Your plan does not include lunch.')
            return redirect('mark_attendance', customer_id=customer_id)
        
        if meal_type == 'DINNER' and not customer.can_mark_dinner():
            messages.error(request, 'Your plan does not include dinner.')
            return redirect('mark_attendance', customer_id=customer_id)
        
        # Check if already marked
        if Attendance.has_marked_today(customer, meal_type):
            messages.warning(request, f'{meal_type.capitalize()} attendance already marked for today.')
            return redirect('mark_attendance', customer_id=customer_id)
        
        # Check time window
        meal_window = 'lunch' if meal_type == 'LUNCH' else 'dinner'
        if not self.is_within_time_window(meal_window):
            messages.error(request, f'{meal_type.capitalize()} attendance can only be marked during designated hours.')
            return redirect('mark_attendance', customer_id=customer_id)
        
        # Mark attendance
        Attendance.objects.create(
            customer=customer,
            meal_type=meal_type
        )
        
        messages.success(request, f'{meal_type.capitalize()} attendance marked successfully! ✓')
        return redirect('mark_attendance', customer_id=customer_id)
    
    @staticmethod
    def is_within_time_window(meal_type):
        """Check if current time is within meal time window"""
        now = timezone.now().time()
        
        if meal_type == 'lunch':
            start = datetime.strptime(settings.LUNCH_START_TIME, '%H:%M').time()
            end = datetime.strptime(settings.LUNCH_END_TIME, '%H:%M').time()
        else:  # dinner
            start = datetime.strptime(settings.DINNER_START_TIME, '%H:%M').time()
            end = datetime.strptime(settings.DINNER_END_TIME, '%H:%M').time()
        
        return start <= now <= end


class AttendanceHistoryView(View):
    """View for customer attendance history"""
    
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, customer_id=customer_id)
        
        # Get attendance records for current month
        today = timezone.localtime(timezone.now()).date()
        attendances = Attendance.objects.filter(
            customer=customer,
            date__month=today.month,
            date__year=today.year
        ).order_by('-date')
        
        # Group by date
        attendance_by_date = {}
        for attendance in attendances:
            date_key = attendance.date
            if date_key not in attendance_by_date:
                attendance_by_date[date_key] = []
            attendance_by_date[date_key].append(attendance.meal_type)
        
        context = {
            'customer': customer,
            'attendance_by_date': attendance_by_date,
            'days_remaining': customer.days_remaining,
            'is_expiring_soon': customer.is_expiring_soon,
        }
        
        return render(request, 'customer/attendance_history.html', context)
