# PDF Portal Setup Guide

Complete step-by-step guide to set up and run the PDF Portal application.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Google OAuth Setup](#google-oauth-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Google account for OAuth setup
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/surendra767116/django12.git
cd django12
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.x
- google-auth
- google-auth-oauthlib
- google-auth-httplib2

### 3. Create Required Directories

```bash
mkdir -p media pdf_data static
```

## Google OAuth Setup

To enable Google authentication, you need to create OAuth credentials:

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "PDF Portal")
4. Click "Create"

### Step 2: Enable Google+ API

1. In the left sidebar, go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and press "Enable"

### Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields (App name, User support email, etc.)
   - Add your email to test users
   - Save and continue
4. Back in "Create OAuth client ID":
   - Application type: "Web application"
   - Name: "PDF Portal"
   - Authorized JavaScript origins: `http://localhost:8000`
   - Authorized redirect URIs: `http://localhost:8000/auth/callback/`
5. Click "Create"
6. **IMPORTANT**: Copy the "Client ID" and "Client Secret" - you'll need these!

### Step 4: Configure OAuth Consent Screen

1. Go to "OAuth consent screen" in the left sidebar
2. Add your application information:
   - App name: PDF Portal
   - User support email: your email
   - Developer contact: your email
3. Add scopes:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
4. Add test users (emails that can log in during development)
5. Save

## Configuration

### Option 1: Environment Variables (Recommended for Production)

Create a `.env` file in the project root (or set environment variables):

```bash
export GOOGLE_OAUTH_CLIENT_ID="your-client-id-here.apps.googleusercontent.com"
export GOOGLE_OAUTH_CLIENT_SECRET="your-client-secret-here"
export ADMIN_EMAILS="admin@example.com,another-admin@example.com"
```

### Option 2: Edit Settings Directly (For Development)

Edit `pdf_portal/settings.py`:

```python
# Find these lines and replace with your values:
GOOGLE_OAUTH_CLIENT_ID = 'your-client-id-here.apps.googleusercontent.com'
GOOGLE_OAUTH_CLIENT_SECRET = 'your-client-secret-here'
ADMIN_EMAILS = ['admin@example.com', 'another-admin@example.com']
```

**Note**: Replace the email addresses with the actual Google email addresses that should have admin access.

## Running the Application

### 1. Verify Configuration

Run the test script to verify everything is set up correctly:

```bash
python test_app.py
```

You should see:
```
✓ All tests passed!
The application is ready to use.
```

### 2. Start the Development Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### 3. Access the Application

Open your web browser and go to:
```
http://localhost:8000
```

You'll be redirected to the login page.

## Usage

### For Students (Regular Users)

1. **Login**:
   - Click the Google Sign-In button
   - Authorize the application
   - You'll be redirected to the home page

2. **Upload PDF**:
   - Click "Choose File" in the upload section
   - Select a PDF file from your computer
   - Click "Upload PDF"
   - The file will appear in the list below

3. **Download PDF**:
   - Find the PDF you want to download
   - Click the "Download" button
   - The file will be downloaded to your computer

4. **Logout**:
   - Click the "Logout" button in the top right

### For Administrators

Administrators have all student features plus:

1. **Access Admin Dashboard**:
   - After login, click "Admin Dashboard" in the navigation
   - View statistics (total PDFs, storage used, user count)

2. **View All PDFs**:
   - See a table with all uploaded PDFs
   - View file details, uploader, and dates

3. **Upload PDFs as Admin**:
   - Use the admin upload form to add PDFs
   - PDFs uploaded by admins are marked accordingly

4. **Delete PDFs**:
   - Click the "Delete" button next to any PDF
   - Confirm the deletion
   - The file and its metadata are permanently removed

## Troubleshooting

### Issue: "Authentication failed: Token verification failed"

**Solution**: 
- Verify your Google OAuth Client ID is correct in settings
- Make sure the redirect URI is exactly: `http://localhost:8000/auth/callback/`
- Check that the Client ID is enabled in Google Cloud Console
- Clear your browser cookies and try again

### Issue: "Admin permissions" error

**Solution**:
- Make sure your email is in the `ADMIN_EMAILS` list in settings
- Logout and login again after adding your email
- Email addresses are case-sensitive and must match exactly

### Issue: Cannot upload files

**Solution**:
- Verify the `media/` directory exists and is writable
- Check file is actually a PDF (must have .pdf extension)
- Make sure the file size is reasonable (not too large)

### Issue: Server won't start

**Solution**:
- Check if another process is using port 8000:
  ```bash
  lsof -i :8000  # On Mac/Linux
  netstat -ano | findstr :8000  # On Windows
  ```
- Use a different port:
  ```bash
  python manage.py runserver 8001
  ```

### Issue: "No module named 'google'"

**Solution**:
- Reinstall dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Issue: PDFs not showing up

**Solution**:
- Check if `pdf_data/pdfs_metadata.json` exists
- Verify file permissions on `pdf_data/` directory
- Check Django logs for errors

## Security Notes

### For Production Deployment

If deploying to production, make sure to:

1. **Change SECRET_KEY**: Generate a new secret key
   ```python
   # In settings.py
   SECRET_KEY = 'your-new-secret-key-here'
   ```

2. **Disable DEBUG**: Set DEBUG to False
   ```python
   DEBUG = False
   ```

3. **Set ALLOWED_HOSTS**: Add your domain
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

4. **Use HTTPS**: Configure SSL certificate and use HTTPS
   - Update Google OAuth redirect URI to use HTTPS
   - Set SECURE_SSL_REDIRECT = True in settings

5. **Use Environment Variables**: Never commit credentials to git
   - Use `.env` file (add to .gitignore)
   - Or use environment variables from your hosting platform

6. **Set up proper file storage**: 
   - Consider using cloud storage (AWS S3, Google Cloud Storage)
   - Set up backup system for PDF files and metadata

7. **Monitor and limit file uploads**:
   - Set MAX_UPLOAD_SIZE in settings
   - Implement rate limiting
   - Add virus scanning for uploaded files

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Python Documentation](https://docs.python.org/3/)

## Support

For issues or questions:
1. Check this guide and README.md
2. Review the troubleshooting section
3. Check Django error logs
4. Create an issue on GitHub repository

## License

This project is for educational purposes.
