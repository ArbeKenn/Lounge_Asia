from django.contrib.auth import authenticate
from rest_framework import serializers
from models import MyUsersManager, User

class UserSer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'firstname','lastname']

class MyUserDetSer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRegSer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username','email','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class UserLogSer(serializers.Serializer):
    class Meta:
        model = User
        email = serializers.CharField(max_length=255)
        password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                data['user'] = user

            data['user'] = user
        return data
