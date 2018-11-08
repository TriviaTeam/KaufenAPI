from django.urls import include, path
from .views import *
from.client_views import *

urlpatterns = [
    path('store/', StoreEndpoint.as_view(), name="store-endpoint"),
    path('products/', ProductsEndpoints.as_view(), name="products-endpoint"),
    path('clients/', ClientEndpoint.as_view(), name="clients-endpoint"),
    path('clients/<str:client_id>/', ClientEndpoint.as_view(), name="clients-endpoint"),
    path('clients/<str:client_id>/orders/', ClientOrdersViewEndpoint.as_view(), name="clients-endpoint"),
    path('clients/<int:client_id>/wallet/', WalletView.as_view(), name="clients-wallet-endpoint"),
    path('orders/', OrderGeneralEndpoints.as_view(), name="orders-endpoint"),
    path('orders/<int:id>/', OrderView.as_view(), name="orders-products-endpoint"),
    path('orders/any/', AnyProductOrdersView.as_view(), name="-any-orders-endpoint"),
    path('orders/any/<int:order_id>/', AnyProductOrdersView.as_view(), name="any-orders-endpoint"),
]
