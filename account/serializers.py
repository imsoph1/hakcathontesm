from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'last_name', 'first_name', 'username')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError('Passwords did not match! ')
        if attrs['password'].isalnum():
            raise serializers.ValidationError('Password filed must contain alpha symbols and numbers!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {'bad_token': _('Token is invalid or expired!')}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class RecoverySerializator(serializers.ModelSerializer):
    email = serializers.CharField(min_length=8, max_length=20,
                                  required=True, write_only=True)
    password = serializers.CharField(min_length=8, max_length=20,
                                     required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=20,
                                      required=True, write_only=True)

    activtion_code = serializers.CharField(min_length=8, max_length=20,
                                           required=True, write_only=True)

    def validate(self, attrs):
        ''' Email '''
        email = attrs.pop('email')
        if attrs['email'] != email:
            raise serializers.ValidationError('email did not match!')
        if '@gmail.com' not in attrs['email']:
            raise serializers.ValidationError('please enter your gmail'
                                              'excemple@gmail.com')

        ''' Activate_code '''
        activation_code2 = attrs.pop('activation_code')
        if attrs['activation_code'] != activation_code2:
            raise serializers.ValidationError('activation_code did not match!')

        ''' Password '''
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError('Passwords did not match!')
        if not attrs['password'].isalnum():
            raise serializers.ValidationError('Password field must contain'
                                              'alpha symbols and numbers!')
        return attrs
