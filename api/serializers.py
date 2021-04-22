from api.models import Component, ComponentReport, WebStore, \
    WebStoreComponent, AssembledConstruction, ConstructionComponent, \
    ConstructionReport, Cart
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class ComponentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentReport
        fields = '__all__'


class WebStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebStore
        fields = '__all__'


class WebStoreComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebStoreComponent
        fields = '__all__'


class AssembledConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssembledConstruction
        fields = '__all__'


class ConstructionComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionComponent
        fields = '__all__'


class ConstructionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionReport
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class AppropriateConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssembledConstruction
        fields = ['id', 'name', 'image']





