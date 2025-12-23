# Django Blog Application

A simple blog application built with Django 3.2.14, ready for deployment on Render.

## Features

- Blog post creation and management
- User authentication
- Admin interface
- Responsive templates

## Local Development

### Prerequisites

- Python 3.9 or higher
- pip

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/surendra767116/django12.git
   cd django12
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory (optional for local development):
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Navigate to the Django project:
   ```bash
   cd django_blog
   ```

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

9. Access the application at `http://localhost:8000`

## Deployment on Render

### Method 1: Using render.yaml (Recommended)

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and set up:
   - A PostgreSQL database
   - A web service with the Django application

### Method 2: Manual Setup

1. **Create a PostgreSQL Database:**
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Name it (e.g., `django-blog-db`)
   - Copy the Internal Database URL

2. **Create a Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name:** django-blog
     - **Runtime:** Python 3
     - **Build Command:** `./build.sh`
     - **Start Command:** `cd django_blog && gunicorn blogproject.wsgi:application`

3. **Set Environment Variables:**
   Add the following environment variables in Render:
   - `SECRET_KEY`: Generate a secure random key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Render URL (e.g., `your-app-name.onrender.com` or use `.onrender.com` to allow all Render subdomains)
   - `DATABASE_URL`: Internal Database URL from PostgreSQL database

4. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - After the first deployment, update the `ALLOWED_HOSTS` environment variable with your actual Render URL if you used `.onrender.com`

### Important Notes for Render Deployment

- The first deployment may take a few minutes
- After deployment, create a superuser by accessing the Render Shell:
  ```bash
  cd django_blog
  python manage.py createsuperuser
  ```
- Static files are served using WhiteNoise
- The database will be PostgreSQL in production
- Make sure to set a strong `SECRET_KEY` in production

## Project Structure

```
django12/
├── django_blog/           # Main Django project directory
│   ├── blog/             # Blog application
│   ├── blogproject/      # Project settings
│   ├── manage.py         # Django management script
│   └── db.sqlite3        # SQLite database (local only)
├── requirements.txt      # Python dependencies
├── build.sh             # Render build script
├── render.yaml          # Render deployment configuration
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Dependencies

- Django 3.2.25 - Web framework (Latest LTS 3.2.x release)
- gunicorn 22.0.0 - WSGI HTTP server
- whitenoise 6.6.0 - Static file serving
- psycopg2-binary 2.9.9 - PostgreSQL adapter
- dj-database-url 2.1.0 - Database URL parsing
- python-decouple 3.8 - Environment variable management

**Note:** Django 3.2.x is an LTS (Long Term Support) version that receives security updates until April 2024. For production applications requiring support beyond this date, consider upgrading to Django 4.2 LTS (supported until April 2026) or later versions.

## Environment Variables

The application uses the following environment variables:

- `SECRET_KEY`: Django secret key (required in production)
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection URL (PostgreSQL in production)

## Security Considerations

- Never commit `.env` files or expose your `SECRET_KEY`
- Always set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` properly
- Use HTTPS in production (Render provides this automatically)

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.
