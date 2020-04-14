from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import StoreUser, CustomerUser


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('email',)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True, help_text=_('Please enter the email in proper email '
                                                                              'format'))
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError(_('No such user found'))

        else:
            if not data.get('password'):
                raise serializers.ValidationError(_("Please fill the password field"))
            elif not data.get('email'):
                raise serializers.ValidationError(_('Please fill the email field'))
        data['user'] = user
        return data

    class Meta:
        model = StoreUser
        fields = ('email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True, help_text=_('Please enter the email in proper email '
                                                                              'format'))
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate_email(self, email):
        existed = StoreUser.objects.filter(email=email).first()
        if existed:
            raise serializers.ValidationError(_('Another user have registered with the same email before!'))
        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError(_("Please fill the password and confirmation !"))
        elif data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError(_("Password does not match"))
        return data

    def create(self, validated_data):
        user = StoreUser(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        CustomerUser.objects.create(user=user)
        Token.objects.create(user=user)
        # send_verification_email.delay(user.id)
        return user

    class Meta:
        model = StoreUser
        fields = ('email', 'password', 'confirm_password',)
        extra_kwargs = {'password': {'write_only': True}}
