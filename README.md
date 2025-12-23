# PDF Portal - Student PDF Management System

A Django-based web application for students to upload and download PDF files with Google OAuth authentication and admin dashboard functionality.

## Features

- 🔐 **Google OAuth Authentication** - Secure login using Google accounts
- 📤 **PDF Upload** - Students can upload PDF files
- 📥 **PDF Download** - Download any uploaded PDF
- 👨‍💼 **Admin Dashboard** - Admin interface for managing PDFs
- 🗑️ **Delete PDFs** - Admins can delete PDF files
- 💾 **No Database** - Uses file-based storage for simplicity
- 📊 **Statistics** - View total PDFs, storage usage, and users

## Requirements

- Python 3.8+
- Django 5.0+
- Google OAuth Client ID and Secret

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/auth/callback/`
6. Copy the Client ID and Client Secret

### 3. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-google-client-id"
export GOOGLE_OAUTH_CLIENT_SECRET="your-google-client-secret"
export ADMIN_EMAILS="admin1@example.com,admin2@example.com"
```

Or edit `pdf_portal/settings.py` directly to set these values.

### 4. Create Required Directories

```bash
mkdir -p media pdf_data static
```

### 5. Run the Application

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

### For Students

1. Visit `http://localhost:8000`
2. Click "Sign in with Google"
3. After authentication, you'll see the home page
4. Upload PDFs using the upload form
5. Download any PDF by clicking the download button

### For Admins

1. Make sure your email is added to `ADMIN_EMAILS` in settings
2. After login, you'll see an "Admin Dashboard" link
3. Admin dashboard shows:
   - Statistics (total PDFs, storage, users)
   - All uploaded PDFs in a table
   - Upload functionality
   - Delete functionality for each PDF

## Project Structure

```
django12/
├── pdf_portal/          # Django project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py
├── pdfs/                # Main application
│   ├── views.py         # All views and logic
│   ├── urls.py          # App URL routing
│   └── ...
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── home.html        # Student dashboard
│   └── admin_dashboard.html  # Admin dashboard
├── media/               # Uploaded PDF files (gitignored)
├── pdf_data/            # JSON metadata files (gitignored)
├── static/              # Static files
└── requirements.txt     # Python dependencies
```

## Technical Details

### No Database Implementation

This application uses a file-based approach instead of a traditional database:

- **PDF Metadata**: Stored in JSON format in `pdf_data/pdfs_metadata.json`
- **User Sessions**: Stored in JSON format in `pdf_data/user_sessions.json`
- **PDF Files**: Stored in the `media/` directory
- **Session Management**: Uses Django's signed cookie sessions

### Security Features

- Google OAuth 2.0 authentication
- CSRF protection on all forms
- Session-based authentication
- Admin authorization checks
- File type validation (PDF only)

### File Structure

Each PDF entry in metadata contains:
- Unique ID (UUID)
- Original filename
- Stored filename
- File size
- Uploader email and name
- Upload timestamp

## Notes

- This implementation does not use a database as per requirements
- Admin users are defined by email addresses in settings
- All PDF files are stored in the `media/` directory
- Metadata is stored in JSON files
- Sessions use signed cookies (no database required)

## Troubleshooting

### Google OAuth not working

1. Verify your Client ID and Secret are correct
2. Check authorized redirect URIs in Google Console
3. Make sure `http://localhost:8000` is in authorized origins
4. Clear browser cookies and try again

### "Admin permissions" error

Make sure your email is in the `ADMIN_EMAILS` environment variable or settings.

### Files not uploading

1. Check if `media/` directory exists and is writable
2. Verify file is a valid PDF
3. Check Django logs for errors

## License

This project is created for educational purposes.
