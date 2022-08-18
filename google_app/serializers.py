from rest_framework import serializers
from google_app.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('number', 'order_number', 'price_dollars', 'price_rubles', 'delivery_time')
