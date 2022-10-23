from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import GenericAPIView
from . import serializers
from django.contrib.auth import get_user_model

from .send_email import send_confirmation_email, send_code_email


User = get_user_model()


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user.email, user.activation_code)
            return Response(serializer.data, status=201)
        return Response('Bad request', status=400)


class ActivationView(APIView):
    permission_class = (permissions.AllowAny,)

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Successfully activated1'}, status=200)
        except User.DoesNotExist:
            return Response({'msg': 'Link expired!'}, status=400)


class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)


class LogoutView(GenericAPIView):
    serializer_class = serializers.LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully logged out!', status=204)


class RecoveryView(APIView):
    permission_classes = (permissions.AllowAny,)

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        User.activation_code = code

    def post(self, request):
        serializer = serializers.RecoverySerializator(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_code_email(user.email, user.activation_code)
            return Response(serializer.data, status=201)
        return Response('Bad request!', status=400)
