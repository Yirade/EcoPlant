# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, RegistrationView, UserDeviceDataView, DeviceDataView, DeviceRegistrationView, UserDevicesView, DeviceSensorDataView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('register/', RegistrationView.as_view(), name='user-register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('device-data/', DeviceDataView.as_view(), name='device-add-data'),
    path('user-device-data/', UserDeviceDataView.as_view(), name='user-device-data'),
    path('register-device/', DeviceRegistrationView.as_view(), name='register-device'),
    path('user-devices/', UserDevicesView.as_view(), name='user-devices'),
    path('device-sensor-data/', DeviceSensorDataView.as_view(), name='device-sensor-data'),
]