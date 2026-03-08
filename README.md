# Monthly Mess Management System

A comprehensive Django-based web application for managing monthly mess subscriptions with customer self-service attendance marking and admin management capabilities.

## Features

### Customer Features
- 4-digit ID-based quick access
- Mark attendance for Lunch/Dinner
- Plan-based meal button enabling
- Duplicate attendance prevention
- Attendance history with calendar view
- Subscription validity tracking

### Admin Features
- Secure admin login
- Real-time dashboard with statistics
- Customer CRUD operations
- Auto-generated 4-digit customer IDs
- Attendance reports and analytics
- UPI QR code generation
- WhatsApp reminder automation

## Tech Stack

- **Backend**: Django 5.0
- **Frontend**: Django Templates + Tailwind CSS
- **Database**: PostgreSQL
- **Payments**: UPI QR Codes
- **Notifications**: Twilio WhatsApp API
- **Deployment**: Render

## Setup Instructions

### 1. Clone and Navigate
```bash
cd e:\Monthly-mess
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your credentials:
# - SECRET_KEY (generate using: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
# - DATABASE_URL (PostgreSQL connection string)
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
```

### 5. Build Tailwind CSS
```bash
# Install Node.js dependencies
npm install

# Build CSS
npm run build:css
```

### 6. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Admin User
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit:
- Customer Interface: http://localhost:8000/
- Admin Interface: http://localhost:8000/admin/

## Configuration

### Payment Rates
- Lunch Only: ₹1,800/month
- Dinner Only: ₹1,800/month
- Both: ₹3,600/month

### Meal Times
- Lunch: 12:00 PM - 3:00 PM
- Dinner: 7:00 PM - 10:00 PM

### WhatsApp Reminders
Automatic reminders are sent 2 days before subscription expiry.

To manually trigger reminders:
```bash
python manage.py send_reminders
```

To set up automated daily reminders, add to cron or use Render's cron jobs:
```
0 9 * * * cd /path/to/project && python manage.py send_reminders
```

## Deployment to Render

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Create Render Account
- Sign up at https://render.com

### 3. Create PostgreSQL Database
- New → PostgreSQL
- Note the Internal Database URL

### 4. Create Web Service
- New → Web Service
- Connect your GitHub repository
- Configure:
  - **Build Command**: `./build.sh`
  - **Start Command**: `gunicorn mess_manager.wsgi:application`
  - **Environment Variables**: Add all from `.env`

### 5. Add Environment Variables
Add these in Render dashboard:
- `SECRET_KEY`
- `DATABASE_URL` (from PostgreSQL service)
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `PYTHON_VERSION=3.11.0`

## Project Structure

```
Monthly-mess/
├── mess_manager/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                  # Main application
│   ├── models.py         # Customer & Attendance models
│   ├── views.py          # Customer views
│   ├── admin_views.py    # Admin views
│   ├── forms.py          # Django forms
│   ├── urls.py           # URL routing
│   ├── utils/            # Utilities
│   │   ├── qr_generator.py
│   │   └── whatsapp.py
│   ├── management/
│   │   └── commands/
│   │       └── send_reminders.py
│   └── templates/        # HTML templates
├── static/               # Static files
├── media/                # Uploaded files & QR codes
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT License
