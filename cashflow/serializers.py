from decimal import Decimal
from rest_framework import serializers
from .models import Cashflow, CashflowType


class CashflowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashflowType
        fields = ['cashflow_type_id', 'cashflow_type',
                  'cashflow_subtype', 'cashflow_is_planned']


class CashflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashflow
        fields = ['id', 'cashflow_description',
                  'cashflow_valid_from',
                  'cashflow_amount', 'cashflow_amount_excl_btw',
                  'cashflow_type']

    cashflow_amount_excl_btw = serializers.SerializerMethodField(
        method_name='subtract_btw')

    def subtract_btw(self, cashflow: Cashflow):
        return cashflow.cashflow_amount * Decimal(0.9)
