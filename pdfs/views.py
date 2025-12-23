from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import os
import json
import uuid
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from functools import wraps


# Utility functions for file-based storage
def get_pdf_metadata_path():
    """Get path to PDF metadata JSON file"""
    path = settings.PDF_STORAGE_PATH
    os.makedirs(path, exist_ok=True)
    return path / 'pdfs_metadata.json'


def load_pdfs_metadata():
    """Load PDFs metadata from JSON file"""
    metadata_file = get_pdf_metadata_path()
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            return json.load(f)
    return []


def save_pdfs_metadata(metadata):
    """Save PDFs metadata to JSON file"""
    metadata_file = get_pdf_metadata_path()
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)


def get_user_sessions_path():
    """Get path to user sessions JSON file"""
    path = settings.PDF_STORAGE_PATH
    os.makedirs(path, exist_ok=True)
    return path / 'user_sessions.json'


def load_user_sessions():
    """Load user sessions from JSON file"""
    sessions_file = get_user_sessions_path()
    if sessions_file.exists():
        with open(sessions_file, 'r') as f:
            return json.load(f)
    return {}


def save_user_sessions(sessions):
    """Save user sessions to JSON file"""
    sessions_file = get_user_sessions_path()
    with open(sessions_file, 'w') as f:
        json.dump(sessions, f, indent=2)


def login_required_custom(view_func):
    """Custom login required decorator"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_email = request.session.get('user_email')
        if not user_email:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Custom admin required decorator"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_email = request.session.get('user_email')
        if not user_email:
            return redirect('login')
        if user_email not in settings.ADMIN_EMAILS:
            messages.error(request, 'You do not have admin permissions.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# Authentication views
def login_view(request):
    """Login page with Google OAuth"""
    if request.session.get('user_email'):
        return redirect('home')
    
    context = {
        'google_client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
    }
    return render(request, 'login.html', context)


def auth_callback(request):
    """Handle Google OAuth callback"""
    token = request.POST.get('credential')
    
    if not token:
        messages.error(request, 'Authentication failed. No token received.')
        return redirect('login')
    
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            settings.GOOGLE_OAUTH_CLIENT_ID
        )
        
        # Get user info
        email = idinfo.get('email')
        name = idinfo.get('name')
        picture = idinfo.get('picture')
        
        # Store user info in session
        request.session['user_email'] = email
        request.session['user_name'] = name
        request.session['user_picture'] = picture
        request.session['is_admin'] = email in settings.ADMIN_EMAILS
        
        # Store in file-based session storage
        sessions = load_user_sessions()
        sessions[email] = {
            'email': email,
            'name': name,
            'picture': picture,
            'last_login': datetime.now().isoformat(),
            'is_admin': email in settings.ADMIN_EMAILS,
        }
        save_user_sessions(sessions)
        
        messages.success(request, f'Welcome, {name}!')
        return redirect('home')
        
    except ValueError as e:
        messages.error(request, f'Authentication failed: {str(e)}')
        return redirect('login')


def logout_view(request):
    """Logout user"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# Main views
@login_required_custom
def home_view(request):
    """Home page showing all PDFs"""
    pdfs = load_pdfs_metadata()
    
    # Sort by upload date (newest first)
    pdfs.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
    
    context = {
        'pdfs': pdfs,
        'user_email': request.session.get('user_email'),
        'user_name': request.session.get('user_name'),
        'user_picture': request.session.get('user_picture'),
        'is_admin': request.session.get('is_admin', False),
    }
    return render(request, 'home.html', context)


@login_required_custom
@require_http_methods(["POST"])
def upload_pdf(request):
    """Handle PDF upload"""
    if 'pdf_file' not in request.FILES:
        messages.error(request, 'No file uploaded.')
        return redirect('home')
    
    pdf_file = request.FILES['pdf_file']
    
    # Validate file type
    if not pdf_file.name.endswith('.pdf'):
        messages.error(request, 'Only PDF files are allowed.')
        return redirect('home')
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{pdf_file.name}"
    
    # Create media directory
    media_path = settings.MEDIA_ROOT
    os.makedirs(media_path, exist_ok=True)
    
    # Save file
    file_path = media_path / filename
    with open(file_path, 'wb+') as destination:
        for chunk in pdf_file.chunks():
            destination.write(chunk)
    
    # Add metadata
    pdfs = load_pdfs_metadata()
    pdf_metadata = {
        'id': file_id,
        'filename': pdf_file.name,
        'stored_filename': filename,
        'size': pdf_file.size,
        'uploaded_by': request.session.get('user_email'),
        'uploaded_by_name': request.session.get('user_name'),
        'uploaded_at': datetime.now().isoformat(),
    }
    pdfs.append(pdf_metadata)
    save_pdfs_metadata(pdfs)
    
    messages.success(request, f'PDF "{pdf_file.name}" uploaded successfully!')
    return redirect('home')


@login_required_custom
def download_pdf(request, file_id):
    """Download a PDF file"""
    pdfs = load_pdfs_metadata()
    
    # Find the PDF
    pdf = None
    for p in pdfs:
        if p['id'] == file_id:
            pdf = p
            break
    
    if not pdf:
        messages.error(request, 'PDF not found.')
        return redirect('home')
    
    # Get file path
    file_path = settings.MEDIA_ROOT / pdf['stored_filename']
    
    if not file_path.exists():
        messages.error(request, 'PDF file not found on server.')
        return redirect('home')
    
    # Return file
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf["filename"]}"'
    return response


@admin_required
@require_http_methods(["POST"])
def delete_pdf(request, file_id):
    """Delete a PDF file (admin only)"""
    pdfs = load_pdfs_metadata()
    
    # Find and remove the PDF
    pdf_to_delete = None
    updated_pdfs = []
    for p in pdfs:
        if p['id'] == file_id:
            pdf_to_delete = p
        else:
            updated_pdfs.append(p)
    
    if not pdf_to_delete:
        messages.error(request, 'PDF not found.')
        return redirect('admin_dashboard')
    
    # Delete physical file
    file_path = settings.MEDIA_ROOT / pdf_to_delete['stored_filename']
    if file_path.exists():
        os.remove(file_path)
    
    # Save updated metadata
    save_pdfs_metadata(updated_pdfs)
    
    messages.success(request, f'PDF "{pdf_to_delete["filename"]}" deleted successfully!')
    return redirect('admin_dashboard')


@admin_required
def admin_dashboard(request):
    """Admin dashboard for managing PDFs"""
    pdfs = load_pdfs_metadata()
    users = load_user_sessions()
    
    # Sort PDFs by upload date (newest first)
    pdfs.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
    
    # Calculate statistics
    total_pdfs = len(pdfs)
    total_size = sum(p.get('size', 0) for p in pdfs)
    total_users = len(users)
    
    context = {
        'pdfs': pdfs,
        'total_pdfs': total_pdfs,
        'total_size': total_size,
        'total_users': total_users,
        'users': users,
        'user_email': request.session.get('user_email'),
        'user_name': request.session.get('user_name'),
        'user_picture': request.session.get('user_picture'),
        'is_admin': True,
    }
    return render(request, 'admin_dashboard.html', context)


@admin_required
@require_http_methods(["POST"])
def admin_upload_pdf(request):
    """Admin upload PDF"""
    return upload_pdf(request)
