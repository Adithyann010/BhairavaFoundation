"""
WSGI config for bairava_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bairava_project.settings')

application = get_wsgi_application()
app = application

# Auto-initialize SQLite database on Vercel Serverless environment
if os.environ.get('VERCEL') == '1':
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        import populate_db
    except Exception as e:
        print(f"Vercel DB initialization error: {e}")
