# Monthly Mess Management System - Setup Guide

## Quick Start (Development)

### 1. Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Create .env File
```powershell
copy .env.example .env
```

Edit `.env` and add:
- Generate SECRET_KEY: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- For development, you can use SQLite (default) or configure PostgreSQL

### 4. Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```powershell
python manage.py createsuperuser
```

### 6. Create Media Directories
```powershell
mkdir media
mkdir media\qr_codes
```

### 7. Run Development Server
```powershell
python manage.py runserver
```

Visit:
- Customer Portal: http://localhost:8000/
- Admin Login: http://localhost:8000/admin/login/
- Django Admin: http://localhost:8000/admin/

## Testing the Application

### Create Test Customer
1. Login to admin panel: http://localhost:8000/admin/login/
2. Go to Dashboard → Add Customer
3. Fill in details (ID will be auto-generated)
4. Save customer

### Test Customer Flow
1. Go to http://localhost:8000/
2. Enter the 4-digit customer ID
3. Mark attendance for lunch/dinner
4. View attendance history

### Test QR Code Generation
1. Go to Customers list
2. Click "QR" next to any customer
3. View generated QR code

### Test Reminder Command
```powershell
python manage.py send_reminders --dry-run
```

## Production Deployment (Render)

See README.md for detailed deployment instructions.

## Troubleshooting

### Issue: Static files not loading
```powershell
python manage.py collectstatic
```

### Issue: Database errors
```powershell
python manage.py migrate --run-syncdb
```

### Issue: QR codes not generating
- Check that `media/qr_codes/` directory exists
- Check file permissions

## Environment Variables Reference

Required for production:
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `TWILIO_ACCOUNT_SID`: Twilio account SID
- `TWILIO_AUTH_TOKEN`: Twilio auth token
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Your domain name

Pre-configured:
- `UPI_ID`: adipatil6464-2@oksbi
- `LUNCH_PRICE`: 1800
- `DINNER_PRICE`: 1800
- `BOTH_PRICE`: 3600
- Meal time windows
