from functools import partial

from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import generics, response, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from users.models import Department, User

from .permissions import IsSameDepartmentOrStaff, IsOwnProfileOrStaff
from .serializers import (DepartmentSerializer, ProfileDetailSerializer,
                          ProfileListSerializer, UserPasswordSerializer,
                          UserSerializer, UserUpdateProfileSerializer)
from .validators import password_validator


class UsersViewSet(viewsets.ModelViewSet):
    """ Displaying all users """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
    permission_classes = (IsAuthenticated,)


class CreateProfile(generics.CreateAPIView):
    """ Generic Create API View.
    Allow a user that is not authenticated to register """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """Create a new user

        Args:
            request: Data for the new user

        Returns:
            response: Serialized data and HTTP status
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
    
        email = data.get('email')
        password = data.get('password')
        department = Department.objects.get(id=data.get('department'))
        extra_fields = {
            "full_name": data.get('full_name'),
            "department": department}

        if User.objects.create_user(email, password, **extra_fields):
            serializer = self.get_serializer(
                User.objects.filter(email=email).first())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ReadProfileList(generics.ListAPIView):
    """ Displaying only full name, and profile identifier """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.filter(id=self.kwargs['pk'])

        if queryset.exists():
            return queryset
        else:
            raise generics.Http404

    serializer_class = ProfileListSerializer
    http_method_names = ['get']


class ReadProfileDetail(generics.ListAPIView):
    """ Displaying all info about an user """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = User.objects.filter(id=self.kwargs['pk'])

        if queryset.exists():
            return queryset
        else:
            raise generics.Http404

    serializer_class = ProfileDetailSerializer
    http_method_names = ['get']


class UserUpdateProfile(generics.RetrieveUpdateAPIView):
    """ Updates an user profile """
    permission_classes = (IsAuthenticated, IsSameDepartmentOrStaff,)
    queryset = User.objects.all()
    serializer_class = UserUpdateProfileSerializer
    lookup_field = 'pk'
    http_method_names = ['put']


class UserChangePassword(generics.UpdateAPIView):
    """ Changes an authenticated user password """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordSerializer
    http_method_names = ['put']

    def get_object(self, queryset=None):

        obj = User.objects.filter(id=self.kwargs['pk']).first()
        if obj is not None:
            return obj
        else:
            raise generics.Http404

    def update(self, request, *args, **kwargs):
        """Updates an user password

        Args:
            request: old and new password to be changed

        Returns:
            response: Serialized data and HTTP status
        """

        old_password = request.data['old_password']
        new_password = request.data['new_password']

        if not password_validator(old_password):
            return Response(
                {'old_password': "The password must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"}, status=status.HTTP_400_BAD_REQUEST)

        if not password_validator(new_password):
            return Response(
                {'new_password': "The password must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"}, status=status.HTTP_400_BAD_REQUEST)

        self.obj = self.get_object()

        if not self.obj.check_password(old_password):
            return Response({"old_password": "The old password didn't match."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.obj.set_password(new_password)
            self.obj.save()

            response = {
                'message': 'Password updated successfully',
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDeleteProfile(generics.DestroyAPIView):
    """Deletes an user profile"""
    permission_classes = (IsAuthenticated, IsOwnProfileOrStaff,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


class DepartmentsViewSet(viewsets.ModelViewSet):
    """ Creates a department"""
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    http_method_names = ['get', 'post']


class DepartmentDeleteProfile(generics.DestroyAPIView):
    """ Deletes a department """
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'pk'
    http_method_names = ['delete']
