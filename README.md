# Django User Profile Application

A Django web application with user profile management featuring a modern, user-friendly interface.

## Features

- User registration with email validation
- User login and logout functionality
- Comprehensive user profile management
- Profile picture upload
- Personal information fields (bio, location, birth date, phone, website)
- Responsive design with Bootstrap 5
- Clean and intuitive user interface
- Automatic profile creation on user registration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/surendra767116/django12.git
cd django12
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to:
- Main application: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Usage

### Registration
1. Navigate to the registration page
2. Fill in the required fields (username, email, password)
3. Click "Sign Up" to create your account

### Login
1. Navigate to the login page
2. Enter your username and password
3. Click "Login"

### Profile Management
1. After logging in, you'll be redirected to your profile page
2. Update your personal information in the form
3. Upload a profile picture
4. Add your bio, location, birth date, phone number, and website
5. Click "Update Profile" to save your changes

## Project Structure

```
django12/
├── manage.py
├── requirements.txt
├── README.md
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── userprofile/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    └── templates/
        └── userprofile/
            ├── base.html
            ├── login.html
            ├── logout.html
            ├── profile.html
            └── register.html
```

## Technologies Used

- Django 6.0.2
- Bootstrap 5.1.3
- SQLite (default database)
- Pillow (for image handling)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
