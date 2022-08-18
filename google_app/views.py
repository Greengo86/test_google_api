from django.http import HttpResponse
from rest_framework import viewsets

from google_app.models import Order
from google_app.serializers import OrderSerializer
from google_app.tasks import start_scrap_spreadsheet


def index(request):
    start_scrap_spreadsheet()
    return HttpResponse("Run scrap info by Google API")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('number')
    serializer_class = OrderSerializer
