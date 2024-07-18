from django.shortcuts import render
from .serializers import CustomerSerializer, RegistrationSerializer, CustomerLoginSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Customer
from django.contrib.auth.models import User

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from django.shortcuts import redirect

# Create your views here.

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class RegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            customer = serializer.create(validated_data=request.data)
            user = customer.user
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))

            try:
                new_uid = urlsafe_base64_decode(uid).decode()
                user = User._default_manager.get(id=new_uid)
            except(User.DoesNotExist):
                user = None
            
            if user is not None and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({'success':'customer created successfully'})
            
        return Response(serializer.errors)


class CustomerLoginView(APIView):

    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate()
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request=request, user=user)
                return Response({'token':token.key, 'user_id':user.id})
            else:
                return Response({'error':'Invalid Credential'})
        return Response(serializer.errors)

class CustomerLogoutView(APIView):

    def get(self, request):
        request.user.auth_token.delete()
        logout(request=request)
        return redirect('login')