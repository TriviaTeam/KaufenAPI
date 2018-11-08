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
			orders = OrderList.objects.filter(client=client)
			any_product_orders = self.get_any_products_orders(client)

			serializer_orders = OrderSerializer(orders, many=True)

			data = {
				"orders":serializer_orders.data,
				"any_product_orders":any_product_orders
			}

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

				if store != False:

					new_product = Product(
						name=data['name'],
						category=data['category'],
						price=data['price'],
						store=store
					)

					new_product.save()

					products.append(new_product)

			else:
				continue
			

		if len(products) > 0:
			serializer = ProductSerializer(products, many=True)
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"mensagem":"erro ao salvar produtos"}, status=status.HTTP_400_BAD_REQUEST)
			

	def get_store_by_name(self, store_id):
		
		try:
			store = Store.objects.get(id=store_id)
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

		return True


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
						"order":serializer.data,
						"products":products
					}
				)

			status_code = status.HTTP_400_BAD_REQUEST

		else:
			order = AnyProductOrder.objects.get(id=order_id)
			serializer = AnyProductOrderSerializer(order)

			data = serializer.data
			status_code = status.HTTP_200_OK

		return Response(data, status=status_code)

	def get_order_products(self,order):

		products = AnyProduct.objects.filter(order=order)
		serializer = AnyProductSerializer(products, many=True)

		return serializer.data

	def post(self, request, order_id=None, format=None):
		
		client = self.get_client(request.data['client_id'])

		if client != False:
			new_order = AnyProductOrder(
				client=client,
				total=0,
				status=StatusCode['in_line'],
			)

			new_order.save()

			products = self.create_any_products(request.data['products'], new_order)

			if len(products) > 0:
				order_serializer = AnyProductOrderSerializer(new_order)
				product_serializer = AnyProductSerializer(products, many=True)

				data = {
					"order":order_serializer.data,
					"products":product_serializer.data
				}

				return Response(data,status=status.HTTP_201_CREATED)

			else:
				return Response({"ERRO":"Não foi possivel criar lista"},status=status.HTTP_400_BAD_REQUEST)

		else:
			return Response({"ERRO":"Cliente não encontrado"},status=status.HTTP_400_BAD_REQUEST)

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