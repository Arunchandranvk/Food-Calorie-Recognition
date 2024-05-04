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
from tensorflow.keras.models import load_model



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
        


from tensorflow.keras.models import load_model
import cv2
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FoodImage
from .serializers import FoodImageSerializer
from .utils import predict_class, predict_volume


@api_view(['POST'])
def CaloriesAdvisorAPI(request):
    if request.method == 'POST' and request.FILES['image']:
        model = load_model('D:/Internship Luminar/Main Projects/Image Food Recognition/food_recognition.h5', compile=False)
        image_file = request.FILES['image']
        img = process_image(image_file)
        pred_value, cal_data = predict_class(model, img)

        if cal_data is not None:
            predicted_volume = predict_volume(img)
            food_image = FoodImage(image=image_file, predicted_food=pred_value, calories_data=cal_data, predicted_volume=predicted_volume)
            food_image.save()
            serializer = FoodImageSerializer(food_image)
            return Response(serializer.data)
        else:
            return Response({"error": "Not a food item!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Image file not provided."}, status=status.HTTP_400_BAD_REQUEST)