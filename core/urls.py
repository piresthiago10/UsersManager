from django.contrib import admin
from django.urls import path, include
from users.api.viewsets import UsersViewSet
from users.api.viewsets import CreateProfile
from users.api.viewsets import DepartmentsViewSet
from users.api.viewsets import ReadProfileList
from users.api.viewsets import ReadProfileDetail
from users.api.viewsets import UserUpdateProfile
from users.api.viewsets import UserChangePassword
from users.api.viewsets import UserDeleteProfile
from users.api.viewsets import DepartmentDeleteProfile
from rest_framework import routers
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='Users')
router.register('departments', DepartmentsViewSet, basename='Departments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls) ),
    path('users/create', CreateProfile.as_view()),
    path('users/<int:pk>/profile/', ReadProfileList.as_view()),
    path('users/<int:pk>/detail/', ReadProfileDetail.as_view()),
    path('users/<int:pk>/update/', UserUpdateProfile.as_view()),
    path('users/<int:pk>/change_password/', UserChangePassword.as_view()),
    path('users/<int:pk>/delete/', UserDeleteProfile.as_view()),
    path('departments/<int:pk>/delete/', DepartmentDeleteProfile.as_view()),
    path('api-token-auth/', views.obtain_auth_token)
]
