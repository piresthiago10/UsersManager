from django.http import response
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)
from users.models import Department, User

class AuthenticatedUsersTestCase(APITestCase):

    def setUp(self):

        email = 'user1@test.com'
        password = '123ABCde'
        extra_fields = {"full_name": 'User Numberone'}

        self.user1 = User.objects.create_superuser(email, password, **extra_fields)
        self.token1 = Token.objects.create(user=self.user1)
        self.api_authentication(self.token1)

        self.department1 = Department.objects.create(department="Creation")
        self.department2 = Department.objects.create(department="Development")
        self.department3 = Department.objects.create(department="Security")

        email = 'user2@test.com'
        password = '123ABChj'
        extra_fields = {"full_name": 'User Numbertwo',
        "department": self.department1,
        "is_staff": True }

        self.user2 = User.objects.create_user(email, password, **extra_fields)
        self.token2 = Token.objects.create(user=self.user2)
        self.api_authentication(self.token2)

    def api_authentication(self, token):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(token))

    def test_read_profile_list(self):
        """Test if a logged in user is allowed to get an user profile list"""
        response = self.client.get('/users/1/profile/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_read_profile_wrong_id_list(self):
        """Test endpoint with an id that doesn't exist"""
        response = self.client.get('/users/15/profile/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_profile_datail(self):
        """Test if a logged user is allowed to get an user profile detail"""
        response = self.client.get('/users/1/detail/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_read_profile_wrong_id_detail(self):
        """Test endpoint with an id that doesn't exist"""
        response = self.client.get('/users/15/detail/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update_profile(self):
        """Test if a logged in user is allowed to update an user profile"""
        data = {
            "full_name": "User Numbertwo Update",
            "email": "user2_update@teste.com.br",
            "department": 2
            }

        response = self.client.put('/users/2/update/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_update_wrong_department_profile(self):
        """Test endpoint with an department id that doesn't exist"""
        data = {
            "full_name": "User Numbertwo Update",
            "email": "user2_update@teste.com.br",
            "department": 7
            }

        response = self.client.put('/users/2/update/', data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_change_password(self):
        """Test if a logged in user is allowed to update his own password"""
        data = {
            "old_password": "123ABChj",
            "new_password": "123ABCaa"   
        }
        response = self.client.put('/users/2/change_password/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_change_wrong_password(self):
        """Test endpoint with an wrong password"""
        data = {
            "old_password": "123ABChh",
            "new_password": "123ABCaa"   
        }
        response = self.client.put('/users/2/change_password/', data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_change_wrong_id_password(self):
        """Test endpoint with an user id that doesn't exist"""
        data = {
            "old_password": "123ABC10",
            "new_password": "123ABCad"   
        }
        response = self.client.put('/users/15/change_password/', data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_change_wrong_pattern_password(self):
        """Test endpoint with a wrong pattern password"""
        data = {
            "old_password": "123ABC10",
            "new_password": "12345"   
        }
        response = self.client.put('/users/2/change_password/', data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_token(self):
        """Test if a logged in user is allowed to delete his own profile"""
        response = self.client.delete('/users/2/delete/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

class UnauthenticatedUsersTestCase(APITestCase):

    def setUp(self):

        self.department1 = Department.objects.create(department="Creation")

        email = 'user2@test.com'
        password = '123ABChj'
        extra_fields = {"full_name": 'User Numbertwo',
        "department": self.department1,
        "is_staff": True }

        self.user2 = User.objects.create_user(email, password, **extra_fields)

    def test_create_user(self):
        """Test if a non logged in user is allowed to create his own profile"""
        data = {
            "full_name": "User Numberone",
            "email": "user1@test.com",
            "password": "123ABC8a",
            "department": 1
        }

        response = self.client.post('/users/create', data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_log_in(self):
        """Test if a non logged in user is allowed to log in """
        data = {
            "username": "user2@test.com",
            "password": "123ABChj",
        }

        response = self.client.post('/api-token-auth/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_read_profile_list(self):
        """Test if a non logged in user is allowed to get a profile list"""
        response = self.client.get('/users/1/profile/')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_read_profile_detail(self):
        """Test if a non logged in user is allowed to get a profile detail"""
        response = self.client.get('/users/1/detail/')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update_profile(self):
        """Test if a non logged in user is allowed to update profile"""
        data = {
            "full_name": "User Numbertwo Update",
            "email": "user2_update@teste.com.br",
            "department": 2
            }

        response = self.client.put('/users/2/update/', data=data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_change_password(self):
        """Test if a non logged in user is allowed to change password"""
        data = {
            "old_password": "123ABChj",
            "new_password": "123ABCaa"   
        }
        response = self.client.put('/users/2/change_password/', data=data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        """Test if a non logged in user is allowed to delete a profile"""
        response = self.client.delete('/users/2/delete/')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

class NonAdminUsersTestCase(APITestCase):

    def setUp(self):

        self.department1 = Department.objects.create(department="Creation")
        self.department2 = Department.objects.create(department="Development")

        email = 'user1@test.com'
        password = '123ABChj'
        extra_fields = {"full_name": 'User Numberone',
        "department": self.department1}

        self.user1 = User.objects.create_user(email, password, **extra_fields)
        self.token1 = Token.objects.create(user=self.user1)
        self.api_authentication(self.token1)

        email = 'user2@test.com'
        password = '123ABChj'
        extra_fields = {"full_name": 'User Numbertwo',
        "department": self.department1}

        self.user2 = User.objects.create_user(email, password, **extra_fields)

        email = 'user3@test.com'
        password = '123ABChj'
        extra_fields = {"full_name": 'User Numberthree',
        "department": self.department2}

        self.user3 = User.objects.create_user(email, password, **extra_fields)

    def api_authentication(self, token):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(token))

    def test_user_update_profile(self):
        """Test if a non admin user is allowed to update his own profile"""
        data = {
            "full_name": "User Numbertwo Update",
            "email": "user2_update@teste.com.br",
            "department": 1
            }

        response = self.client.put('/users/2/update/', data=data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_update_different_department_profile(self):
        """Test if a non admin user is allowed to update another department user profile"""
        data = {
            "full_name": "User Numberthree Update",
            "email": "user3_update@teste.com.br",
            "department": 2
            }

        response = self.client.put('/users/3/update/', data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        """Test if a non admin user is allowed to delete his own profile"""
        response = self.client.delete('/users/1/delete/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_usern(self):
        """Test if a non admin user is allowed to delete another user profile"""
        response = self.client.delete('/users/2/delete/')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

class DepartmentsAdminUserTestCase(APITestCase):

    def setUp(self):

        self.department1 = Department.objects.create(department="Creation")

        email = 'user1@test.com'
        password = '123ABCde'
        extra_fields = {
            "full_name": 'User Numberone',
            "department": self.department1,
            "is_staff": True
            }

        self.user = User.objects.create_user(email, password, **extra_fields)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))

    def test_create_department(self):
        """Test if an admin user is allowed to create a department"""
        data = {
            "department": "Development"
        }

        response = self.client.post("/departments/", data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_department_empty(self):
        """ Test an endpoint with empty department name """
        data = {
            "department": ""
        }

        response = self.client.post("/departments/", data=data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_department(self):
        """Test if an admin user is allowed to delete a department"""
        response = self.client.delete('/departments/1/delete/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_department_not_found(self):
        """Test endpoint with an department id that doesn't exist"""
        response = self.client.delete('/departments/3/delete/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

class DepartmentsNonAdminUserTestCase(APITestCase):

    def setUp(self):

        self.department1 = Department.objects.create(department="Creation")

        email = 'user1@test.com'
        password = '123ABCde'
        extra_fields = {
            "full_name": 'User Numberone',
            "department": self.department1,
            }

        self.user = User.objects.create_user(email, password, **extra_fields)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))

    def test_create_department(self):
        """Test if a non admin user is allowed to create a department"""
        data = {
            "department": "Development"
        }

        response = self.client.post("/departments/", data=data)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_department(self):
        """Test if a non admin user is allowed to delete a department"""
        response = self.client.delete('/departments/1/delete/')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)