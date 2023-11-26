from decimal import Decimal
from rest_framework import serializers
from .models import TransactionType, TransactionPlanned, TransactionVariable, BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'date', 'amount']


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
