from rest_framework import serializers
from .models import User
from uuid import uuid4



class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta(object):
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = uuid4().hex[:-6]
            user.set_password(password)
            user.save()
        return user
