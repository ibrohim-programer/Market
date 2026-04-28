from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView ,CreateAPIView , ListAPIView , UpdateAPIView , RetrieveAPIView
from django.contrib.auth import get_user_model 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny , IsAuthenticated
from drf_spectacular.utils import extend_schema

from .serializers import *

User = get_user_model()
@extend_schema(tags=["Auth - Register - Login - OTP"],)
class RegisterView(CreateAPIView):    
    serializer_class = RegisterSerializers
    permission_classes = [AllowAny]
    
@extend_schema(tags=["Auth - Register - Login - OTP"],)
class LoginView(GenericAPIView):
    serializer_class = LoginSerializers
    permission_classes = [AllowAny]
    def post(self , request):
        try:
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("Success", status=200)
        except Exception as e:
            return Response({"Error" : str(e)} , status=400)
    
@extend_schema(tags=["Auth - Register - Login - OTP"],)
class VerifyOtpView(GenericAPIView):
    serializer_class = VerifyOtpSerializers
    permission_classes = [AllowAny]
    def post(self , request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email = email)
        refrish_token = RefreshToken.for_user(user)
        return Response({"User" : user.username , "Role" : user.role , "Access Token" : str(refrish_token.access_token)} , status=200)
    
@extend_schema(tags=["Auth - Forgot/Verify Password"],)  
class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer  
    permission_classes = [AllowAny]
    def post(self , request):
        try:
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("Success", status=200)
        except Exception as e:
            return Response({"Error" : str(e)} , status=400)
        
@extend_schema(tags=["Auth - Forgot/Verify Password"],)  
class VerifyPasswordView(GenericAPIView):
    serializer_class = VerifyPasswordSerializers
    permission_classes = [AllowAny]
    def post(self , request) :
        try:
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            user = User.objects.get(email = email)
            user.set_password(new_password)
            user.save()
            return Response({"message" : "Password updated successfully ."} , status=200)
        except Exception as e:
            return Response({"Error" : str(e)} , status=400)

@extend_schema(tags=["Auth - Profile"],)
class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    
@extend_schema(tags=["Auth - Profile"],)
class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileSerializers
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request , *args , **kwargs)