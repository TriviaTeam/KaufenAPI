import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import *


class ClientEndpoint(APIView):

	def get(self, request, format=None):

		clients = Client.objects.all()
		serializer = ClientSerializer(clients, many=True)

		return Response(serializer.data)

	def post(self, request, format=None):
		
		serializer = ClientSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

			if self.check_data(data):

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
					continue

			else:
				continue
			

		if len(products) > 0:
			serializer = ProductSerializer(products, many=True)
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"mensagem":"erro ao salvar produtos"}, status=status.HTTP_400_BAD_REQUEST)
			

	def get_store_by_name(self, store_name):
		
		try:
			store = Store.objects.get(name=store_name)
			print("Loja já cadastrada")
			return store

		except Store.DoesNotExist:
			return False

	def check_data(self, data):
		
		attrs = ['name','category','price','store']
		data_attrs = list(data.keys())
		for attr in data_attrs:
			if attr not in attrs:
				return False
			else:
				continue


class OrderGeneralEndpoints(APIView):

	def get(self, request, format=None):

		orders = OrderList.objects.all()
		serializer = OrderSerializer(orders, many=True)

		return Response(serializer.data)

	def post(self, request, format=None):
		
		order_data = request.data

		if self.check_data(order_data):

			client = self.get_client(order_data['client'])

			if client:
				products = self.get_products(order_data['products'])

				if len(products)>0:
					order = OrderList(
						client=client,
						total=0
					)

					for product in products:
						order.products.add(product)
						order.total += product.price

					order.client = client
					order.save()

					serializer = OrderSerializer(order)

					return Response(serializer.data, status=status.HTTP_201_CREATED)

				else:
					return Response({"mensagem":"erro ao adicionar produtos à lista"}, status=status.HTTP_400_BAD_REQUEST)

			else:
				return Response({"mensagem":"erro ao adicionar cliente à lista"}, status=status.HTTP_400_BAD_REQUEST)

		else:
			return Response({"mensagem":"erro ao salvar lista de compras"}, status=status.HTTP_400_BAD_REQUEST)

	def check_data(self, data):
		
		attrs = ['client','products']
		data_attrs = list(data.keys())
		for attr in data_attrs:
			if attr not in attrs:
				return False
			else:
				continue

	def get_products(self, products_ids):
		
		products = []

		for id in products_ids:

			try:
				product = Product.objects.get(id=id)
				products.append(product)

			except Product.DoesNotExist:
				continue

		return products

	def get_client(self, client_id):

		try:
			client = Client.objects.get(id=id)
			return client

		except Client.DoesNotExist:
			return False