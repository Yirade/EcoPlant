# users/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Device

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None
        
        try:
            device = Device.objects.get(api_key=api_key)
        except Device.DoesNotExist:
            raise AuthenticationFailed('Invalid API key.')
        
        return (device, None)