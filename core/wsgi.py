import os
import socketio

from django.core.wsgi import get_wsgi_application
from chat.views import sio


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)