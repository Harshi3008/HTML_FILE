# Library Management System

A comprehensive library management system built with Django that provides an efficient way to manage books, members, and library operations.

## ✨ Features

- **User Authentication**
  - User registration and login
  - QR code based authentication
  - OTP verification
  - Role-based access control (Admin/User)

- **Book Management**
  - Add, edit, and delete books
  - Categorize books by category and sub-category
  - Track book availability
  - Book search functionality

- **Issue/Return System**
  - Issue books to members
  - Track due dates
  - Handle book returns
  - Reissue books
  - Pre-booking system

- **Additional Features**
  - Blog system for library news
  - Event management
  - Team information
  - Donation management
  - Contact form
  - Book suggestions from users

## 🛠️ Tech Stack

- **Backend**: Django 5.0
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (Development), PostgreSQL (Production-ready)
- **Authentication**: Django Auth + Custom QR Code Auth
- **Payment Integration**: Razorpay
- **Other Tools**:
  - Pillow for image processing
  - ReportLab for PDF generation
  - OpenPyXL for Excel operations
  - Python Decouple for environment variables

## 📦 Dependencies

List of main Python packages used in the project:

```
Django==5.0.0
python-dotenv==1.0.0
Pillow==10.0.0
whitenoise==6.5.0
dj-database-url==2.0.0
gunicorn==20.1.0
twilio==8.10.0
django-crispy-forms==2.1
crispy-bootstrap5==2024.2
python-decouple==3.8
qrcode==8.2
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual Environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HTML_FILE
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root and add:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📚 Project Structure

```
Litrery/               # Main project directory
├── Land/              # Main app
│   ├── migrations/    # Database migrations
│   ├── static/        # Static files (CSS, JS, images)
│   ├── templates/     # HTML templates
│   ├── __init__.py
│   ├── admin.py      # Admin configurations
│   ├── apps.py       # App config
│   ├── models.py     # Database models
│   ├── urls.py      # App URLs
│   └── views.py     # View functions
├── Litrery/          # Project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py   # Project settings
│   ├── urls.py      # Main URLs
│   └── wsgi.py
├── manage.py         # Django management script
└── requirements.txt  # Project dependencies
```

## 🔒 Authentication Flow

1. **Regular Login**
   - Username/Password authentication
   - OTP verification for added security

2. **QR Code Login**
   - Generate unique QR code for each user
   - Scan QR code to authenticate
   - Secure token-based verification

## 📱 Admin Features

- Manage books (add, edit, delete)
- Handle book issues and returns
- Manage users and permissions
- View reports and analytics
- Manage blog posts and events
- Handle book donations

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap 5
- All contributors who helped in development

---

Developed with ❤️ by Your Organization
