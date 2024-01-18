from rest_framework import serializers

class AvailableTimesSerializer(serializers.Serializer):
    id_date = serializers.DateField(format='%Y-%m-%d')