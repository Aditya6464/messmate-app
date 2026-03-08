"""
Django management command to send WhatsApp reminders to customers
whose subscriptions are expiring in 2 days
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Customer
from core.utils.qr_generator import generate_upi_qr, get_plan_amount
from core.utils.whatsapp import send_renewal_reminder
from django.conf import settings


class Command(BaseCommand):
    help = 'Send WhatsApp reminders to customers with expiring subscriptions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without actually sending messages',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Calculate target date (2 days from now)
        target_date = timezone.now().date() + timedelta(days=2)
        
        # Find customers expiring on target date
        expiring_customers = Customer.objects.filter(
            is_active=True,
            end_date=target_date
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Found {expiring_customers.count()} customers expiring on {target_date}'
            )
        )
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No messages will be sent'))
        
        success_count = 0
        error_count = 0
        
        for customer in expiring_customers:
            try:
                # Get plan amount
                amount = get_plan_amount(customer.plan_type)
                
                # Generate QR code
                qr_path = generate_upi_qr(customer, amount)
                
                # Build full URL (you may need to configure your domain)
                # For production, use your actual domain
                qr_url = f"{settings.MEDIA_URL}{qr_path}"
                
                # In production, you'd use request.build_absolute_uri()
                # For now, we'll use a placeholder or environment variable
                base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
                full_qr_url = f"{base_url}{qr_url}"
                
                self.stdout.write(
                    f'Processing: {customer.name} ({customer.customer_id}) - {customer.phone_number}'
                )
                
                if not dry_run:
                    # Send WhatsApp reminder
                    result = send_renewal_reminder(customer, full_qr_url)
                    
                    if result:
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ Sent reminder to {customer.name}')
                        )
                        success_count += 1
                    else:
                        self.stdout.write(
                            self.style.ERROR(f'✗ Failed to send reminder to {customer.name}')
                        )
                        error_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(f'[DRY RUN] Would send to {customer.name}')
                    )
                    success_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error processing {customer.name}: {str(e)}')
                )
                error_count += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'Successfully processed: {success_count}'))
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))
        self.stdout.write('='*50)
