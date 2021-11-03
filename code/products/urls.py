from django.urls import path
from .views import *
app_name = 'product'
urlpatterns = [
    path('home/', home),
    path('customer/', cus_list, name='cus-list'),
    path('customer/<int:id>/', print_cus_info, name='cus-info'),
    path('history/', order_history, name='order-history'),
    path('history/<int:id>', print_order),
    path('order/<int:id>/', create_order, name='create-order'),
    path('order/<int:id>/confirm/', check_order, name='check-order'),
    path('place/', place_list, name='place-list'),
    path('place/<int:id>/', get_cus_info, name='get-cusinfo'),
    path('place/confirm/', confirm_reserve),
    path('place/reservation/', reservation),
    path('pay/', pay),
    path('pay/fetch/', pay_fetch),
    path('pay/confirm/', pay_confirm),
]
