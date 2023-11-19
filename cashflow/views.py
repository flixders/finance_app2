
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from cashflow.filters import CashflowFilter
from cashflow.pagination import DefaultPagination
from cashflow.models import Cashflow, CashflowType
from cashflow.serializers import CashflowSerializer, CashflowTypeSerializer


class CashflowViewSet(ModelViewSet):
    queryset = Cashflow.objects.all()
    serializer_class = CashflowSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CashflowFilter
    search_fields = ['cashflow_description']
    ordering_fields = ['id', 'cashflow_amount']
    pagination_class = DefaultPagination

    def destroy(self, request, *args, **kwargs):
        if Cashflow.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Cashflow cannot be deleted'})

        return super().destroy(request, *args, **kwargs)


class CashflowTypeList(ListAPIView):
    queryset = CashflowType.objects.all()
    serializer_class = CashflowTypeSerializer
