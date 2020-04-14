from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import logout
from rest_framework.viewsets import ModelViewSet
from .models import CustomerUser
from .serializers import RegisterSerializer, LoginSerializer, CustomerProfileSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        email = serializer.validated_data['email']
        return Response(data={'message': "dear user with email {0},"
                                         " you successfully registered".format(email)},
                        status=status.HTTP_201_CREATED, headers=headers)

# TODO: add list of orders in profile
class ProfileView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    http_method_names = ['get', 'put']

    def get_queryset(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').replace('Token', '').strip()
        user = CustomerUser.objects.get(id=Token.objects.get(key=token).user_id)
        return Response(self.serializer_class(user.customerProfile).data)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)


class logoutView(APIView):

    def post(self, request):
        logout(request)
        return Response(data={'message': 'Sucessfully logged out'}, status=status.HTTP_200_OK)
