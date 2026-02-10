from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile


class UserProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_created_automatically(self):
        """Test that a profile is automatically created when a user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_profile_str(self):
        """Test the string representation of the profile"""
        self.assertEqual(str(self.user.profile), 'testuser Profile')
    
    def test_profile_fields(self):
        """Test profile fields can be updated"""
        profile = self.user.profile
        profile.bio = 'Test bio'
        profile.location = 'Test City'
        profile.phone_number = '1234567890'
        profile.website = 'https://example.com'
        profile.save()
        
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.location, 'Test City')
        self.assertEqual(profile.phone_number, '1234567890')
        self.assertEqual(profile.website, 'https://example.com')


class UserProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_view_get(self):
        """Test registration view loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/register.html')
    
    def test_register_view_post(self):
        """Test user can register"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_view(self):
        """Test login view loads correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/login.html')
    
    def test_profile_view_requires_login(self):
        """Test profile view requires authentication"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_view_authenticated(self):
        """Test authenticated user can view profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userprofile/profile.html')
    
    def test_profile_update(self):
        """Test user can update their profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Updated bio',
            'location': 'New City',
            'phone_number': '9876543210',
            'website': 'https://newsite.com'
        })
        
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.profile.bio, 'Updated bio')
        self.assertEqual(self.user.profile.location, 'New City')


class UserProfileFormTests(TestCase):
    def test_user_register_form_valid(self):
        """Test registration form with valid data"""
        from .forms import UserRegisterForm
        form = UserRegisterForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertTrue(form.is_valid())
    
    def test_user_register_form_invalid_email(self):
        """Test registration form with invalid email"""
        from .forms import UserRegisterForm
        form = UserRegisterForm(data={
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertFalse(form.is_valid())
    
    def test_user_register_form_password_mismatch(self):
        """Test registration form with mismatched passwords"""
        from .forms import UserRegisterForm
        form = UserRegisterForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpass123',
            'password2': 'differentpass123'
        })
        self.assertFalse(form.is_valid())

