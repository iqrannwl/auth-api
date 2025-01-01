from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import CustomUser
from .utils import Util

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "name", "password", "image", "phone"]

    def create(self, validated_data):
        return super().create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = CustomUser
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["image","name", "phone"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(style={"input_type":"password"}, write_only=True, max_length=255)
    password = serializers.CharField(style={"input_type":"password"}, write_only=True, max_length=255)
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True, max_length=255)

    class Meta:
        model = CustomUser
        fields = ["old_password", "password", "password2"]


    def validate(self, attrs):
        old_password = attrs.get("old_password")
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect")
        if password != password2:
            raise serializers.ValidationError("Password and confirm password don't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            body = 'Click Following Link to Reset Your Password '+link
            data = {
            'subject':'Reset Your Password',
            'body':body,
            'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError({"password": "Password and Confirm Password don't match"})

        try:
            id = smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=id)
        except (DjangoUnicodeDecodeError, CustomUser.DoesNotExist):
            raise serializers.ValidationError({"token": "Token is not Valid or Expired"})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"token": "Token is not Valid or Expired"})

        user.set_password(password)
        user.save()
        return attrs
