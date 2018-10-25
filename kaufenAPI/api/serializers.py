from .models import *
from rest_framework import serializers

class StoreSerializer(serializers.ModelSerializer):

	class Meta:

		model = Store
		fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

	store = StoreSerializer()

	class Meta:

		model = Product
		fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):

	class Meta:

		model = Client
		fields = '__all__'