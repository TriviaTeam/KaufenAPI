import requests
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import *
from .statuscode import StatusCode


class AnyProductOrdersView(APIView):

	def get(self, request, order_id=None, format=None):
		pass

	def post(self, request, order_id=None, format=None):
		pass