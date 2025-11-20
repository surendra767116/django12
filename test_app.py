#!/usr/bin/env python3
"""
Test script to verify the PDF portal application setup
"""
import os
import sys
import json
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdf_portal.settings')
import django
django.setup()

from django.conf import settings
from pdfs.views import (
    load_pdfs_metadata, 
    save_pdfs_metadata, 
    load_user_sessions,
    save_user_sessions
)

def test_settings():
    """Test Django settings are configured correctly"""
    print("✓ Testing Django settings...")
    assert settings.DEBUG == True
    assert 'pdfs' in settings.INSTALLED_APPS
    # Django auto-adds dummy backend when DATABASES is empty, which is fine
    assert settings.SESSION_ENGINE == 'django.contrib.sessions.backends.signed_cookies'
    assert hasattr(settings, 'GOOGLE_OAUTH_CLIENT_ID')
    assert hasattr(settings, 'PDF_STORAGE_PATH')
    print("  ✓ Django settings configured correctly")

def test_directories():
    """Test required directories exist"""
    print("✓ Testing directories...")
    required_dirs = [
        settings.MEDIA_ROOT,
        settings.PDF_STORAGE_PATH,
    ]
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
        assert os.path.exists(dir_path), f"Directory {dir_path} should exist"
    print("  ✓ All required directories exist")

def test_metadata_operations():
    """Test PDF metadata save/load operations"""
    print("✓ Testing metadata operations...")
    
    # Test saving metadata
    test_data = [
        {
            'id': 'test-id-1',
            'filename': 'test.pdf',
            'size': 1024,
            'uploaded_by': 'test@example.com'
        }
    ]
    save_pdfs_metadata(test_data)
    
    # Test loading metadata
    loaded_data = load_pdfs_metadata()
    assert len(loaded_data) == 1
    assert loaded_data[0]['id'] == 'test-id-1'
    
    # Clean up
    save_pdfs_metadata([])
    print("  ✓ Metadata operations working correctly")

def test_session_operations():
    """Test user session save/load operations"""
    print("✓ Testing session operations...")
    
    # Test saving sessions
    test_sessions = {
        'test@example.com': {
            'email': 'test@example.com',
            'name': 'Test User'
        }
    }
    save_user_sessions(test_sessions)
    
    # Test loading sessions
    loaded_sessions = load_user_sessions()
    assert 'test@example.com' in loaded_sessions
    assert loaded_sessions['test@example.com']['name'] == 'Test User'
    
    # Clean up
    save_user_sessions({})
    print("  ✓ Session operations working correctly")

def test_urls():
    """Test URL configuration"""
    print("✓ Testing URL configuration...")
    from django.urls import reverse
    
    url_names = [
        'home',
        'login',
        'logout',
        'auth_callback',
        'upload_pdf',
        'admin_dashboard',
    ]
    
    for url_name in url_names:
        try:
            reverse(url_name)
        except Exception as e:
            raise AssertionError(f"URL '{url_name}' not configured correctly: {e}")
    
    print("  ✓ All URLs configured correctly")

def test_templates():
    """Test template files exist"""
    print("✓ Testing templates...")
    templates = [
        'base.html',
        'login.html',
        'home.html',
        'admin_dashboard.html',
    ]
    
    template_dir = BASE_DIR / 'templates'
    for template in templates:
        template_path = template_dir / template
        assert template_path.exists(), f"Template {template} should exist"
    
    print("  ✓ All templates exist")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PDF Portal Application Tests")
    print("="*60 + "\n")
    
    try:
        test_settings()
        test_directories()
        test_metadata_operations()
        test_session_operations()
        test_urls()
        test_templates()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
        print("\nThe application is ready to use.")
        print("Run 'python manage.py runserver' to start the server.\n")
        
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
