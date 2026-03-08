"""
Admin views for customer and attendance management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from django.http import HttpResponse
from .models import Customer, Attendance
from .forms import CustomerForm
from .utils.qr_generator import generate_upi_qr, get_plan_amount
from .utils.whatsapp import send_payment_qr
from django.conf import settings
import csv
from datetime import datetime, timedelta


class AdminDashboardView(LoginRequiredMixin, View):
    """Admin dashboard with statistics"""
    
    def get(self, request):
        today = timezone.localtime(timezone.now()).date()
        
        # Get today's counts
        lunch_count = Attendance.get_today_count('LUNCH')
        dinner_count = Attendance.get_today_count('DINNER')
        total_count = Attendance.get_today_count()
        
        # Get active customers
        active_customers = Customer.objects.filter(is_active=True).count()
        
        # Get expiring customers (within 2 days)
        expiring_customers = Customer.objects.filter(
            is_active=True,
            end_date__lte=today + timedelta(days=2),
            end_date__gte=today
        ).order_by('end_date')
        
        # Recent attendance
        recent_attendance = Attendance.objects.select_related('customer').order_by('-marked_at')[:10]
        
        context = {
            'lunch_count': lunch_count,
            'dinner_count': dinner_count,
            'total_count': total_count,
            'active_customers': active_customers,
            'expiring_customers': expiring_customers,
            'recent_attendance': recent_attendance,
        }
        
        return render(request, 'admin_panel/dashboard.html', context)


class CustomerListView(LoginRequiredMixin, View):
    """List all customers"""
    
    def get(self, request):
        customers = Customer.objects.all().order_by('-created_at')
        
        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            customers = customers.filter(
                Q(customer_id__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
        
        # Filter by plan
        plan_filter = request.GET.get('plan', '')
        if plan_filter:
            customers = customers.filter(plan_type=plan_filter)
        
        # Filter by status
        status_filter = request.GET.get('status', '')
        if status_filter == 'active':
            customers = customers.filter(is_active=True)
        elif status_filter == 'inactive':
            customers = customers.filter(is_active=False)
        
        context = {
            'customers': customers,
            'search_query': search_query,
            'plan_filter': plan_filter,
            'status_filter': status_filter,
        }
        
        return render(request, 'admin_panel/customer_list.html', context)


class CustomerCreateView(LoginRequiredMixin, View):
    """Create new customer"""
    
    def get(self, request):
        form = CustomerForm()
        return render(request, 'admin_panel/customer_form.html', {'form': form, 'action': 'Create'})
    
    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer created successfully! ID: {customer.customer_id}')
            return redirect('admin_customer_list')
        return render(request, 'admin_panel/customer_form.html', {'form': form, 'action': 'Create'})


class CustomerEditView(LoginRequiredMixin, View):
    """Edit existing customer"""
    
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(instance=customer)
        return render(request, 'admin_panel/customer_form.html', {
            'form': form,
            'customer': customer,
            'action': 'Edit'
        })
    
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('admin_customer_list')
        return render(request, 'admin_panel/customer_form.html', {
            'form': form,
            'customer': customer,
            'action': 'Edit'
        })


class CustomerDeleteView(LoginRequiredMixin, View):
    """Delete customer"""
    
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer_id = customer.customer_id
        customer.delete()
        messages.success(request, f'Customer {customer_id} deleted successfully!')
        return redirect('admin_customer_list')


class GenerateQRView(LoginRequiredMixin, View):
    """Generate and display QR code for customer"""
    
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        amount = get_plan_amount(customer.plan_type)
        
        # Generate QR code
        qr_path = generate_upi_qr(customer, amount)
        qr_url = f"{settings.MEDIA_URL}{qr_path}"
        
        context = {
            'customer': customer,
            'amount': amount,
            'qr_url': qr_url,
            'qr_path': qr_path,
        }
        
        return render(request, 'admin_panel/qr_code.html', context)


class SendQRWhatsAppView(LoginRequiredMixin, View):
    """Send QR code via WhatsApp"""
    
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        amount = get_plan_amount(customer.plan_type)
        
        # Generate QR code
        qr_path = generate_upi_qr(customer, amount)
        
        # Get full URL for QR code
        qr_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{qr_path}")
        
        # Send via WhatsApp
        result = send_payment_qr(customer, qr_url)
        
        if result:
            messages.success(request, f'QR code sent to {customer.phone_number} via WhatsApp!')
        else:
            messages.error(request, 'Failed to send WhatsApp message. Please check Twilio configuration.')
        
        return redirect('admin_customer_list')


class AttendanceReportView(LoginRequiredMixin, View):
    """View attendance reports"""
    
    def get(self, request):
        # Get date range from query params
        today = timezone.localtime(timezone.now()).date()
        start_date = request.GET.get('start_date', today.replace(day=1).isoformat())
        end_date = request.GET.get('end_date', today.isoformat())
        meal_type = request.GET.get('meal_type', '')
        
        # Parse dates
        start_date = datetime.fromisoformat(start_date).date()
        end_date = datetime.fromisoformat(end_date).date()
        
        # Get attendance records
        attendances = Attendance.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).select_related('customer')
        
        if meal_type:
            attendances = attendances.filter(meal_type=meal_type)
        
        # Calculate statistics
        total_attendance = attendances.count()
        lunch_count = attendances.filter(meal_type='LUNCH').count()
        dinner_count = attendances.filter(meal_type='DINNER').count()
        
        # Group by date
        attendance_by_date = {}
        for attendance in attendances.order_by('-date'):
            date_key = attendance.date
            if date_key not in attendance_by_date:
                attendance_by_date[date_key] = {'lunch': 0, 'dinner': 0, 'records': []}
            
            if attendance.meal_type == 'LUNCH':
                attendance_by_date[date_key]['lunch'] += 1
            else:
                attendance_by_date[date_key]['dinner'] += 1
            
            attendance_by_date[date_key]['records'].append(attendance)
        
        context = {
            'start_date': start_date,
            'end_date': end_date,
            'meal_type': meal_type,
            'total_attendance': total_attendance,
            'lunch_count': lunch_count,
            'dinner_count': dinner_count,
            'attendance_by_date': attendance_by_date,
        }
        
        return render(request, 'admin_panel/attendance_report.html', context)


class ExportAttendanceCSVView(LoginRequiredMixin, View):
    """Export attendance to CSV"""
    
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        meal_type = request.GET.get('meal_type', '')
        
        # Get attendance records
        attendances = Attendance.objects.all().select_related('customer')
        
        if start_date:
            attendances = attendances.filter(date__gte=start_date)
        if end_date:
            attendances = attendances.filter(date__lte=end_date)
        if meal_type:
            attendances = attendances.filter(meal_type=meal_type)
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Customer ID', 'Customer Name', 'Meal Type', 'Marked At'])
        
        for attendance in attendances.order_by('-date'):
            writer.writerow([
                attendance.date,
                attendance.customer.customer_id,
                attendance.customer.name,
                attendance.meal_type,
                attendance.marked_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
