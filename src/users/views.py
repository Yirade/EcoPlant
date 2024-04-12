# users/views.py

from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SensorDataSerializer
from .authentication import APIKeyAuthentication
from rest_framework.permissions import IsAuthenticated
from .mqtt_utils import publish_command_to_device
from .models import Device, SensorData
from .serializers import UserLoginSerializer, UserRegistrationSerializer, SensorDataSerializer, DeviceSerializer

class TokenCheckView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'valid': True}, status=status.HTTP_200_OK)
    
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    
class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            if 'username' in errors and 'A user with that username already exists.' in errors['username']:
                return Response({'detail': 'A user with that username already exists.'}, status=status.HTTP_409_CONFLICT)
            elif 'email' in errors and 'Enter a valid email address.' in errors['email']:
                return Response({'detail': 'Enter a valid email address.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
def api_key_required(f):
    def wrap(request, *args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key and Device.objects.filter(api_key=api_key).exists():
            return f(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Invalid or missing API key'}, status=401)
    return wrap

class UserDeviceDataView(ListAPIView):
    serializer_class = SensorDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SensorData.objects.filter(device__owner=user)
    
class DeviceDataView(APIView):
    authentication_classes = [APIKeyAuthentication]

    def post(self, request, format=None):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            if isinstance(request.user, Device):
                serializer.save(device=request.user)
                return Response({"message": "Data received"}, status=200)
            else:
                return Response({"error": "Device not authenticated"}, status=401)
        return Response(serializer.errors, status=400)
    
class DeviceRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        device_name = request.data.get('name', 'Pineapple')

        device = Device.objects.create(
            name=device_name,
            owner=request.user
        )

        return Response({
            "device_id": device.device_id,
            "api_key": device.api_key
        })
    
class UserDevicesView(ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(owner=user)
    

class DeviceSensorDataView(APIView):
    serializer_class = SensorDataSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        device_id = request.data.get('device_id')
        if not device_id:
            raise NotFound(detail="Device ID not provided")

        sensor_data = SensorData.objects.filter(device__device_id=device_id)
        serializer = self.serializer_class(sensor_data, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
        })
    
class DeviceCommandView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        device_id = request.data.get('device_id')
        command = request.data.get('command')
        publish_command_to_device(device_id, command)
        return Response({'message': 'Command sent successfully'}, status=200)