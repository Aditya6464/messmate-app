"""
WhatsApp messaging using Twilio API
"""
from twilio.rest import Client
from django.conf import settings
import os


def get_twilio_client():
    """Initialize and return Twilio client"""
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        raise ValueError("Twilio credentials not configured")
    
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_whatsapp_message(to_number, message):
    """
    Send WhatsApp message via Twilio
    
    Args:
        to_number: Recipient phone number (with country code)
        message: Message text
    
    Returns:
        Message SID if successful, None otherwise
    """
    try:
        client = get_twilio_client()
        
        # Ensure number has whatsapp: prefix
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
        
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=to_number
        )
        
        return message.sid
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        return None


def send_whatsapp_media(to_number, message, media_url):
    """
    Send WhatsApp message with media (QR code)
    
    Args:
        to_number: Recipient phone number
        message: Message text
        media_url: Public URL to media file
    
    Returns:
        Message SID if successful, None otherwise
    """
    try:
        client = get_twilio_client()
        
        # Ensure number has whatsapp: prefix
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
        
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=to_number,
            media_url=[media_url]
        )
        
        return message.sid
    except Exception as e:
        print(f"Error sending WhatsApp media: {e}")
        return None


def send_renewal_reminder(customer, qr_code_url):
    """
    Send subscription renewal reminder with QR code
    
    Args:
        customer: Customer instance
        qr_code_url: Public URL to QR code image
    
    Returns:
        Message SID if successful, None otherwise
    """
    from .qr_generator import get_plan_amount
    
    amount = get_plan_amount(customer.plan_type)
    plan_name = dict(customer.PLAN_CHOICES).get(customer.plan_type)
    
    message = f"""
🔔 *Subscription Renewal Reminder*

Hello {customer.name}!

Your mess subscription is expiring soon.

📅 *End Date:* {customer.end_date.strftime('%d %b %Y')}
📋 *Plan:* {plan_name}
💰 *Amount:* ₹{amount}

Please scan the QR code to renew your subscription.

Thank you! 🙏
    """.strip()
    
    return send_whatsapp_media(
        to_number=customer.phone_number,
        message=message,
        media_url=qr_code_url
    )


def send_payment_qr(customer, qr_code_url):
    """
    Send payment QR code to customer
    
    Args:
        customer: Customer instance
        qr_code_url: Public URL to QR code image
    
    Returns:
        Message SID if successful, None otherwise
    """
    from .qr_generator import get_plan_amount
    
    amount = get_plan_amount(customer.plan_type)
    plan_name = dict(customer.PLAN_CHOICES).get(customer.plan_type)
    
    message = f"""
💳 *Payment QR Code*

Hello {customer.name}!

Your Customer ID: *{customer.customer_id}*

📋 *Plan:* {plan_name}
💰 *Amount:* ₹{amount}

Please scan the QR code below to make payment.

Thank you! 🙏
    """.strip()
    
    return send_whatsapp_media(
        to_number=customer.phone_number,
        message=message,
        media_url=qr_code_url
    )
