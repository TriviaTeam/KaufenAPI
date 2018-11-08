import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import *
from . statuscode import StatusCode


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


	def get_any_products_orders(self, client):

		orders = AnyProductOrder.objects.filter(client=client)
		serializer = AnyProductOrderSerializer(orders, many=True)

		return serializer.data


class ClientOrdersViewEndpoint(APIView):

	def get(self, request, client_id=None, format=None):

		data = {}

		if client_id == None:
			data = {"ERRO":"Cliente não especificado"}

		else:
			client = Client.objects.get(id=client_id)
			orders = OrderList.objects.filter(client=client)
			any_product_orders = self.get_any_products_orders(client)

			serializer_orders = OrderSerializer(orders, many=True)

			data = {
				"orders":serializer_orders.data,
				"any_product_orders":any_product_orders
			}

		return Response(data)