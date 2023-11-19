from django_filters.rest_framework import FilterSet
from .models import Cashflow


class CashflowFilter(FilterSet):
    class Meta:
        model = Cashflow
        fields = {'id': ['exact'],
                  'cashflow_description': ['exact'],
                  'cashflow_valid_from': ['exact', 'gte', 'lte'],
                  'cashflow_amount': ['exact', 'gte', 'lte'],
                  'cashflow_type': ['exact']}
