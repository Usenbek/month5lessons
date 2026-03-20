import requests
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import OAuthCodeSerializer
from rest_framework import status
from django.utils import timezone


User = get_user_model()

class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        
        # Exchange the authorization code for an access token
        token_response = requests.post(
            url = 'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': 'секрет',
                'client_secret': "секрет",
                'redirect_uri': 'http://localhost:8000/api/v1/users/google-login',
                'grant_type': 'authorization_code',
            }
        )
        
        token_response_data = token_response.json()
        access_token = token_response_data.get('access_token')
        
        if not access_token:
            return Response({'error': 'invalid access token'}, status=400)
        
        # Use the access token to get user info
        user_info_response = requests.get(
            url = 'https://www.googleapis.com/oauth2/v3/userinfo',
            params={'alt': 'json'}, 
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()
        
        user_info = user_info_response
        email = user_info.get('email')
        first_name = user_info.get('given_name')
        last_name = user_info.get('family_name')


        if not email:
            return Response({'error': 'Failed to obtain user email'}, status=400)
        
        # Get or create the user
        user, created = User.objects.get_or_create(email=email, defaults={
            'username': email,
            'first': first_name,
            'last_name': last_name,
            'is_active': True,
        })

        user.last_login = timezone.now()
        user.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })