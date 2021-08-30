from django.db import models
from django.db.models import fields
from rest_framework import serializers
from users.models import User, Department
from .validators import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'password', 'email', 'department']

    def validate(self, data):
        """Data validations 

        Args:
            data (dict): values ​​to be validated

        Raises:
            serializers.ValidationError: Error generated if the value does not match the validation

        Returns:
            dict: values validated
        """
        full_name = data['full_name']
        password = data['password']

        try:
            department = data['department']
        except KeyError:
            raise serializers.ValidationError(
                {'department': "The request must have a department field."})

        if not full_name_validator(full_name):
            raise serializers.ValidationError(
                {'full_name': "This field must be alphanumeric."})

        if not password_validator(password):
            raise serializers.ValidationError(
                {'password': "The password must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"})

        return data
        
class UserUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'department']

class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name']

class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
