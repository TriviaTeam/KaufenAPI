from .models import *
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):

	class Meta:

		model = Client
		fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):

	class Meta:

		model = Store
		fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

	store = StoreSerializer()

	class Meta:

		model = Product
		fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

	products = ProductSerializer(many=True)
	client = ClientSerializer()

	class Meta:

		model = OrderList
		fields = '__all__'


class AnyProductSerializer(serializers.ModelSerializer):

	class Meta:

		model = AnyProduct
		fields = ['id', 'name', 'where_to_find']


class AnyProductOrderSerializer(serializers.ModelSerializer):

	products = ProductSerializer(many=True)
	client = ClientSerializer()

	class Meta:

		model = AnyProductOrder
		fields = '__all__'