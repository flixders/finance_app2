from decimal import Decimal
from rest_framework import serializers
from .models import Cashflow, CashflowType
from .models import TransactionType, TransactionPlanned, TransactionVariable, BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['date', 'amount']


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['transaction_type_id', 'type_name',
                  'subtype_name', 'is_planned']


class TransactionPlannedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionPlanned
        fields = ['id', 'amount',
                  'payment_term', 'date_valid_from',
                  'date_valid_up_including', 'description',
                  'transaction_type']


class TransactionVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionVariable
        fields = ['id', 'amount',
                  'date', 'description',
                  'transaction_type']


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
