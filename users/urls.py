from django.urls import path, re_path
from .views import RegisterView, LoginAPIView, logoutView, ProfileView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

# routers = DefaultRouter()
# routers.register('profile/register', ProfileView,basename='address')

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register_user"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('logout/',logoutView.as_view(),name='logout'),
]
# urlpatterns += routers.urls