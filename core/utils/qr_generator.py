"""
QR Code Generator for UPI Payments
"""
import qrcode
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
import os


def generate_upi_qr(customer, amount):
    """
    Generate UPI QR code for payment
    
    Args:
        customer: Customer instance
        amount: Payment amount in rupees
    
    Returns:
        Path to saved QR code image
    """
    # UPI payment URL format
    upi_url = f"upi://pay?pa={settings.UPI_ID}&pn=MessManager&am={amount}&cu=INR&tn=Payment for {customer.name} ({customer.customer_id})"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Create filename
    filename = f"qr_{customer.customer_id}_{amount}.png"
    filepath = os.path.join('qr_codes', filename)
    
    # Ensure directory exists
    qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
    os.makedirs(qr_dir, exist_ok=True)
    
    # Save file
    full_path = os.path.join(qr_dir, filename)
    with open(full_path, 'wb') as f:
        f.write(buffer.getvalue())
    
    return filepath


def get_plan_amount(plan_type):
    """
    Get payment amount based on plan type
    
    Args:
        plan_type: Customer plan type
    
    Returns:
        Amount in rupees
    """
    plan_prices = {
        'LUNCH_ONLY': settings.LUNCH_PRICE,
        'DINNER_ONLY': settings.DINNER_PRICE,
        'BOTH': settings.BOTH_PRICE,
    }
    return plan_prices.get(plan_type, 0)
