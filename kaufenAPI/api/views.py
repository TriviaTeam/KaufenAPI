import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import *

class StoreEndpoint(APIView):

	def get(self, request, format=None):

		stores = Store.objects.all()
		serializer = StoreSerializer(stores, many=True)

		return Response(serializer.data)

	def post(self, request, format=None):

		serializer = StoreSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsEndpoints(APIView):

	def get(self, request, format=None):

		products = Product.objects.all()
		serializer = ProductSerializer(products, many=True)

		return Response(serializer.data)

	def post(self, request, format=None):
		
		products_data = request.data
		products = []

		for data in products_data:

			store = self.get_store_by_name(data['store'])

			if store:

				new_product = Product(
					name=data['name'],
					category=data['category'],
					price=data['price']
				)
				
				new_product.store = store
				new_product.save()

				products.append(new_product)

			else:
				break

		if len(products) > 0:
			serializer = ProductSerializer(products, many=True)
			return Response(serializer.data)

		return Response({"mensagem":"erro ao salvar produtos"})
			

	def get_store_by_name(self, store_name):
		
		try:
			store = Store.objects.get(name=store_name)
			print("Loja já cadastrada")
			return store

		except Store.DoesNotExist:
			return False
		