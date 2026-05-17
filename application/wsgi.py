"""
WSGI config for application project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
from django.contrib.auth import get_user_model
from django.core.management import call_command
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

application = get_wsgi_application()

if os.environ.get('RENDER'):
    print("--- STARTING DEPLOYMENT AUTOMATION ---")
    
    # 1. Run Database Migrations Automatically
    try:
        print("Applying database migrations...")
        call_command('migrate', interactive=False)
        print("Migrations applied successfully!")
    except Exception as e:
        print(f"Migration error: {e}")

    # 2. Create Admin Superuser Automatically
    try:
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser account for {username}...")
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superuser created successfully!")
        else:
            print("Superuser already exists, skipping creation.")
    except Exception as e:
        print(f"Superuser creation error: {e}")
        
    print("--- DEPLOYMENT AUTOMATION COMPLETE ---")
