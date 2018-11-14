import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .statuscode import StatusCode

from .serializers import(
	ClientSerializer, ProductSerializer,
	OrderSerializer, AnyProductOrderSerializer,
	AnyProductSerializer, WalletSerializer
)

from .models import (
	Product, Client,
	Wallet, OrderList,
	AnyProductOrder, AnyProduct,	
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

			orders = OrderList.objects.filter(client=client)
			serializer_orders = OrderSerializer(orders, many=True)
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

	def get_any_products_orders(self, client):

		data = []
		any_product_orders = AnyProductOrder.objects.filter(client=client)

		for order in any_product_orders:
				serializer = AnyProductOrderSerializer(order)
				products = self.get_order_products(order)
				data.append(
					{
						"order":{
							"order-info":serializer.data,
							"products":products
						}
					}
				)

		return data

	def get_order_products(self,order):

		products = AnyProduct.objects.filter(order=order)
		serializer = AnyProductSerializer(products, many=True)

		return serializer.data


class WalletView(APIView):

	def get(self, request, client_id, format=None):

		client = self.get_client(client_id)

		if client == False:
			return Response({"MENSAGEM DE ERRO":"Cliente não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			wallet = Wallet.objects.get(client=client)
			serializer = WalletSerializer(wallet)

			return Response(serializer.data)

	def post(self, request, client_id, format=None):
		
		client = self.get_client(client_id)
		
		if client == False:
			return Response({"MENSAGEM DE ERRO":"Cliente não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

		else:
			wallet_data = request.data

			wallet = Wallet(
				client=client,
				cvv=wallet_data['cvv'],
				credit_card_number=wallet_data['credit_card_number']
			)

			wallet.save()

			serializer = WalletSerializer(wallet)

			return Response(serializer.data, status=status.HTTP_201_CREATED)

	def get_client(self, client_id):

		try:
			client = Client.objects.get(id=client_id)
			return Client.objects.get(id=client_id)
		except Client.DoesNotExist:
			return False