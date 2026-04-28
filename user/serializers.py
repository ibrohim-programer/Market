from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from common.utils import *

 
User = get_user_model()


class RegisterSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only = True , required = True)
    class Meta:
        model = User
        fields = [ "id",'email',"username" , "password" , "password2" , "phone"]   

       
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("The passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
    
class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField(write_only = True , required = True)
    password = serializers.CharField(write_only = True , required = True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            User.objects.get(email = email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email mavjud emas?")
        return attrs
    
    def create(self, validated_data):
        try:
            email = validated_data['email']
            otp = cashe_otp(email)
            send_mail(
                subject="Bizni ilovamizga xushkelibsiz otp kodingiz shu yerda .",
                message=f"OTP CODE:{otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
                )
            user = User.objects.get(email = email)
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))
        
class VerifyOtpSerializers(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']
        if not verify_otp(email , otp):
            raise serializers.ValidationError("Email yoki otp xato ?")
        return attrs
    


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only = True , required = True)        
    username = serializers.CharField(write_only = True , required = True)        
    def validate_email(self, value):
        if not User.objects.filter(email = value).exists():
            raise serializers.ValidationError("Bu email mavjud emas .")
        return value
    def create(self, validated_data):
        try:
            email = validated_data["email"]
            username = validated_data["username"]
            user = User.objects.get(email=email , username=username)
            otp = cashe_otp(email)
            send_mail(
                subject="Parolni tiklash uchun OTP kodingiz:",
                message=f"OTP CODE: {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Email yoki username noto'g'ri.")
        except Exception as e:
            raise serializers.ValidationError(str(e))
        
class VerifyPasswordSerializers(serializers.Serializer):
    email = serializers.EmailField(write_only = True , required = True)        
    username = serializers.CharField(write_only = True , required = True)  
    otp = serializers.CharField(write_only = True , required = True)  
    new_password = serializers.CharField(write_only = True , required = True)
    confirm_password = serializers.CharField(write_only = True , required = True)
    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']
        if not verify_otp(email,otp):
              raise serializers.ValidationError("Email yoki otp xato ?")  
            
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords to not match.")
        return attrs
        
class ProfileSerializers(serializers.ModelSerializer):
    username = serializers.CharField(read_only =True)
    class Meta:
        model = User
        fields =["id","email","username","phone","name","birthday","bio"]
        read_only_fields = ['id' , 'email' , 'created_at' , ]