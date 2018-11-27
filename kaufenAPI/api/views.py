import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import AnyProduct, AnyProductOrder, Client 
from .serializers import AnyProductSerializer, AnyProductOrderSerializer
from .statuscode import StatusCode


class AnyProductOrdersView(APIView):

	def get(self, request, order_id=None, format=None):
		
		if order_id == None:

			orders = AnyProductOrder.objects.all()
			serializer = AnyProductOrderSerializer(orders, many=True)
			data = serializer.data
			status_code = status.HTTP_200_OK

		else:

			order = self.get_order(order_id)

			if order != False:
				serializer = AnyProductOrderSerializer(order)
				data = serializer.data
				status_code = status.HTTP_200_OK
			else:
				data={"ERRO":"ORDEM NÃO ENCONTRADA"}
				status_code = status.HTTP_400_BAD_REQUEST

		return Response(data, status=status_code)

	def post(self, request, format=None):

		client_id = request.data['client_id']
		products_data = request.data['products']

		client = self.get_client(client_id)

		if client != False:
			products = self.create_products(products_data)

			if len(products) > 0:

				order = self.create_new_order(client, products)
				serializer = AnyProductOrderSerializer(order)
				data=serializer.data
				status_code = status.HTTP_200_OK

			else:
				data={"ERRO":"NENHUM PRODUTO INFORMADO"}
				status_code = status.HTTP_400_BAD_REQUEST

		else:
			data={"ERRO":"CLIENTE NÃO ENCONTRADO"}
			status_code = status.HTTP_400_BAD_REQUEST

		return Response(data, status=status_code)


	def get_order(self, order_id):
		
		try:
			order = AnyProductOrder.objects.get(id=order_id)
			return order

		except AnyProductOrder.DoesNotExist:
			return False

	def get_client(self, client_id):
		
		try:
			client = Client.objects.get(id=client_id)
			return client

		except Client.DoesNotExist:
			return False

	def create_products(self, products_data):

		products = []
		
		for data in products_data:
			product = AnyProduct(
				name=data['name'],
				where_to_find=data['where_to_find'],
				price_estimative=data['price_estimative']
			)

			product.save()
			products.append(product)

		return products

	def create_new_order(self, client, products):

		total = 0

		for product in products:
			total += product.price_estimative
		
		order = AnyProductOrder(
			client=client,
			products=products,
			total=total,
			status=StatusCode['in_line']
		)

		order.save()

		return order
