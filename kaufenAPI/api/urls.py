from django.urls import include, path
from .views import *

urlpatterns = [
    path('store/', StoreEndpoint.as_view(), name="store-endpoint"),
    path('products/', ProductsEndpoints.as_view(), name="store-endpoint")
]
