from rest_framework import serializers
from site_app import models

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MyUser
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = '__all__'


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Master
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    class Meta:
        model = models.Schedule
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    master = MasterSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)
    class Meta:
        model = models.Record
        fields = '__all__'
