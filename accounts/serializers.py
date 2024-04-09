from rest_framework import serializers
from .models import *



class  UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=CustUser
        fields=["first_name","email","username","password"]    

    def create(self, validated_data):
        return  CustUser.objects.create_user(**validated_data) 
