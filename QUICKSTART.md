# Quick Start Guide - Run Locally

## 🚀 Start the Application

### Step 1: Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```

### Step 2: Start Development Server
```powershell
python manage.py runserver
```

The server will start at: **http://localhost:8000/**

---

## 🔑 Login Credentials

**Admin Account (Already Created)**:
- Username: `admin`
- Password: `admin123`

---

## 📱 Access Points

### Customer Portal
- **URL**: http://localhost:8000/
- **What to do**: Enter a 4-digit customer ID to mark attendance
- **Note**: You need to create a customer first from the admin panel

### Admin Panel
- **URL**: http://localhost:8000/admin/login/
- **Login**: Use credentials above
- **Features**:
  - Dashboard with statistics
  - Add/Edit/Delete customers
  - Generate QR codes
  - View attendance reports

### Django Admin (Optional)
- **URL**: http://localhost:8000/admin/
- **Login**: Same credentials
- **Use**: Direct database management

---

## 📝 Quick Test Flow

1. **Start Server** (in terminal):
   ```powershell
   .\venv\Scripts\activate
   python manage.py runserver
   ```

2. **Open Browser** → http://localhost:8000/admin/login/

3. **Login** with admin/admin123

4. **Create a Test Customer**:
   - Click "Add Customer" button
   - Fill in:
     - Name: Test User
     - Phone: +919876543210
     - Plan: Both (Lunch + Dinner)
     - Start Date: Today
     - End Date: 30 days from now
     - Lunch Time: 12:00
     - Dinner Time: 19:00
   - Save (Note the auto-generated 4-digit ID)

5. **Test Customer Portal**:
   - Go to http://localhost:8000/
   - Enter the 4-digit ID
   - Mark attendance for lunch/dinner

6. **View Reports**:
   - Go back to admin dashboard
   - Click "View Reports"
   - See the attendance you just marked

---

## 🛑 Stop the Server

Press `Ctrl + C` in the terminal where the server is running

---

## 💡 Tips

- **Time Windows**: Attendance can only be marked during:
  - Lunch: 12:00 PM - 3:00 PM
  - Dinner: 7:00 PM - 10:00 PM
  
- **To test outside time windows**: Edit the times in `.env` or temporarily modify `settings.py`

- **Database**: Using SQLite (db.sqlite3) for development - no PostgreSQL needed locally

- **QR Codes**: Will be saved to `media/qr_codes/` folder

- **WhatsApp**: Won't work without Twilio credentials, but you can test QR generation

---

## 🔧 Troubleshooting

**Server won't start?**
```powershell
python manage.py migrate
```

**Need to reset admin password?**
```powershell
python manage.py changepassword admin
```

**Want to create another admin user?**
```powershell
python manage.py createsuperuser
```
