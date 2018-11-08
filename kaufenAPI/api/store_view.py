import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import StoreSerializer
from .statuscode import StatusCode
from .models import Store


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