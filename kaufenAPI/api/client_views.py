import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .statuscode import StatusCode

from .serializers import(
	ClientSerializer, ProductSerializer,
	OrderSerializer, AnyProductOrderSerializer,
	AnyProductSerializer
)

from .models import (
	Product, Client,
	OrderList, AnyProductOrder, AnyProduct,	
)


class ClientEndpoint(APIView):

	def get(self, request, client_id=None, format=None):

		data = {}

		if client_id == None:
			clients = Client.objects.all()
			serializer = ClientSerializer(clients, many=True)
			data = serializer.data

		else:
			client = Client.objects.get(id=client_id)
			serializer = ClientSerializer(client)
			data = serializer.data

		return Response(data)

	def post(self, request, format=None):
		
		serializer = ClientSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientOrdersViewEndpoint(APIView):

	def get(self, request, client_id=None, format=None):

		data = {}

		try:

			client = Client.objects.get(id=client_id)

			orders = self.get_orders(client)
			any_product_orders = self.get_any_products_orders(client)

			data = {
				"orders":serializer_orders.data,
				"any_product_orders":any_product_orders
			}

			status_code = status.HTTP_200_OK

		except Client.DoesNotExist:

			data = {"ERRO":"CLIENTE NÃO ENCONTRADO"}
			status_code = status.HTTP_400_BAD_REQUEST

		return Response(data, status=status_code)

	def get_orders(self, client):

		orders = OrderList.objects.filter(client=client)
		serializer = OrderSerializer(orders, many=True)

		return serializer.data


	def get_any_products_orders(self, client):

		any_product_orders = AnyProductOrder.objects.filter(client=client)
		serializer = AnyProductOrderSerializer(any_product_orders, many=True)

		return serializer.data