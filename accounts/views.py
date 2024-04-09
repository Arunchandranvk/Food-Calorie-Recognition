from django.shortcuts import render
from .models import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .utils import *


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Ensure token creation or retrieval is properly handled
        token, created = Token.objects.get_or_create(user=user)


        # Extract user information for response
        username = user.username
        first_name = user.first_name
        email = user.email

        # Return response with token and user data
        return Response({
            'status': 1,
            'token': token.key,
            'data': {
                'first_name': first_name,
                'username': username,
                'email': email,
            }
        })
    


class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'status':1,'data':serializer.data})
        else:
            error_messages = ' '.join([error for errors in serializer.errors.values() for error in errors])
            return Response(data={'status':0,'msg': error_messages}, status=status.HTTP_400_BAD_REQUEST)      
        




class CaloriesAdvisorAPI(APIView):
    def post(self, request):
        uploaded_file = request.FILES.get('image')
        if uploaded_file:
            # Process the uploaded image and extract information
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            return Response({'response': response}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

