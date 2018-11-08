import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .statuscode import StatusCode
from .serializers import OrderSerializer
from .models import Product, Client, OrderList 


class OrderGeneralEndpoints(APIView):

	def get(self, request, format=None):

		orders = OrderList.objects.all()
		serializer = OrderSerializer(orders, many=True)

		return Response(serializer.data)

	def post(self, request, format=None):
		
		order_data = request.data

		if self.check_data(order_data):

			client = self.get_client(order_data['client'])

			if (client != False):
				products = self.get_products(order_data['products'])

				if len(products)>0:
					order = OrderList(
						client=client,
						status=StatusCode['in_line'],
						total=0
					)

					order.save()

					for product in products:
						order.products.add(product)
						order.total += product.price

					order.client = client
					order.save()

					serializer = OrderSerializer(order)

					return Response(serializer.data, status=status.HTTP_201_CREATED)

				else:
					return Response({"MENSAGEM DE ERRO":"erro ao adicionar produtos à lista"}, status=status.HTTP_400_BAD_REQUEST)

			else:
				return Response({"MENSAGEM DE ERRO":"erro ao adicionar cliente à lista"}, status=status.HTTP_400_BAD_REQUEST)

		else:
			return Response({"MENSAGEM DE ERRO":"erro ao salvar lista de compras"}, status=status.HTTP_400_BAD_REQUEST)

	def check_data(self, data):
		
		attrs = ['client','products']
		data_attrs = list(data.keys())
		for attr in data_attrs:
			if attr not in attrs:
				return False
			else:
				continue
		return True

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
			client = Client.objects.get(id=client_id)
			return client

		except Client.DoesNotExist:
			return False


class OrderView(APIView):

	def get(self, request, id=None, format=None):

		data = {}

		if id==None:
			data = {"ERRO":"Lista não encontrada"}
			status_code = status.HTTP_400_BAD_REQUEST
		else:
			order = OrderList.objects.get(id=id)
			serializer = OrderSerializer(order)
			data = serializer.data
			status_code = status.HTTP_200_OK

		return Response(data, status=status_code)

	def post(self, request, id=None, format=None):
		
		data = {}

		if id==None:
			data = {"ERRO":"Lista não encontrada"}
			status_code = status.HTTP_400_BAD_REQUEST
		else:
			order = OrderList.objects.get(id=id)
			products = self.get_products(request.data['products'])
			for product in products:
				order.products.add(product)
				order.total += product.price
				order.save()

			serializer = OrderSerializer(order)
			data = serializer.data
			status_code = status.HTTP_201_CREATED

		return Response(data,status=status_code)

	def delete(self, request, id=None, format=None):
		
		if id==None:
			data = {"ERRO":"Lista não encontrada"}
		else:
			order = OrderList.objects.get(id=id)
			products = self.get_products(request.data['products'])
			for product in products:
				order.products.remove(product)
				order.total -= product.price
				order.save()

			serializer = OrderSerializer(order)
			data = serializer.data

		return Response(data)

	def get_products(self, products_ids):
		
		products = []

		for id in products_ids:

			try:
				product = Product.objects.get(id=id)
				products.append(product)

			except Product.DoesNotExist:
				continue

		return products