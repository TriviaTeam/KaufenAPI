import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import *
from .statuscode import StatusCode


class AnyProductOrdersView(APIView):

	def get(self, request, order_id=None, format=None):

		data = []
		
		if order_id==None:
			orders = AnyProductOrder.objects.all()
			for order in orders:
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

			status_code = status.HTTP_400_BAD_REQUEST

		else:
			order = self.get_order(order_id)

			if order !=False:
				order_serializer = AnyProductOrderSerializer(order)
				products = AnyProduct.objects.filter(order=order)
				products_serializer = AnyProductSerializer(products, many=True)

				data = {
					"order":{
						"order-info":order_serializer.data,
						"products":products_serializer.data
					}
				}

				status_code = status.HTTP_200_OK

			else:
				data = {"ERRO":"Ordem não encontrada"}
				status_code=status.HTTP_400_BAD_REQUEST

		return Response(data, status=status_code)

	def post(self, request, order_id=None, format=None):
		
		client = self.get_client(request.data['client_id'])

		if client != False:

			if order_id != None:
				order = self.get_order(order_id)

				if order!=False:
					products = self.create_any_products(request.data['products'], order)
					self.return_response_created_products(products, order)
				else:
					return Response({"ERRO":"Ordem não encontrada"},status=status.HTTP_400_BAD_REQUEST)
			else:
				order = self.create_new_order(request, client)
				products = self.create_any_products(request.data['products'], order)
				self.return_response_created_products(products, order)

		else:
			return Response({"ERRO":"Cliente não encontrado"},status=status.HTTP_400_BAD_REQUEST)

	def get_order_products(self,order):

		products = AnyProduct.objects.filter(order=order)
		serializer = AnyProductSerializer(products, many=True)

		return serializer.data

	def create_new_order(self, request, client):
		
		new_order = AnyProductOrder(
			client=client,
			total=0,
			status=StatusCode['in_line'],
		)

		new_order.save()

		return new_order

	def create_any_products(self, products_data, order):

		created_products = []
		
		for data in products_data:
			
			new_product = AnyProduct(
				name=data['name'],
				where_to_find=data['where_to_find'],
				order=order
			)

			new_product.save()

			created_products.append(new_product)

		return created_products

	def get_client(self, client_id):

		try:
			client = Client.objects.get(id=client_id)
			return client

		except Client.DoesNotExist:
			return False

	def get_order(self, order_id):

		try:
			order = AnyProductOrder.objects.get(id=order_id)
			return order

		except AnyProductOrder.DoesNotExist:
			return False

	def return_response_created_products(self, products, order):

		if len(products) > 0:
			order_serializer = AnyProductOrderSerializer(order)
			product_serializer = AnyProductSerializer(products, many=True)

			data = {
				"order":order_serializer.data,
				"products":product_serializer.data
			}

			return Response(data,status=status.HTTP_201_CREATED)

		else:
			return Response({"ERRO":"Não foi possível adicionar produtos à lista"},status=status.HTTP_400_BAD_REQUEST)