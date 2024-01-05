from rest_framework import serializers
from .models import *

class ProfileSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
