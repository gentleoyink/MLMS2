from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token  # Import Token
from rest_framework.response import Response
from rest_framework.views import APIView



class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Login successful, generate and return token
            token, _ = Token.objects.get_or_create(user=user)  # Generate a token for the user
            print("Generated Token:", token.key)  # Print the token to the console


            # Create a dictionary containing user information
            user_data = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                # Add any other fields you want to include
            }

            response = Response({"user": user_data}, status=status.HTTP_200_OK)
            response.set_cookie('auth_token', token.key, httponly=True, path='/', domain='http://localhost:4200')
            return response
        else:
            # Invalid login
            return Response({"error": "Invalid login"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')
        return response
