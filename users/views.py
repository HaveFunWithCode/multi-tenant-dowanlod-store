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


class ProfileView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer
    http_method_names = ['get', 'put']

    def get_queryset(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').replace('Token', '').strip()
        user = CustomerUser.objects.get(id=Token.objects.get(key=token).user_id)
        return Response(self.serializer_class(user.customerProfile).data)


# TODO: should add check is_verified
class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class logoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(data={'success': 'Sucessfully logged out'}, status=status.HTTP_200_OK)

# def verifyemail(request, uuid):
#     try:
#         user = CustomerUser.objects.get(verification_uuid=uuid, is_verified=False)
#     except CustomerUser.DoesNotExist:
#         raise Http404("User does not exist or is already verified")
#     user.is_verified = True
#     user.save()
#     return redirect('profile')
