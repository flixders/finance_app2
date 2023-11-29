from decimal import Decimal
from rest_framework import serializers
from .models import TransactionType, TransactionPlanned, TransactionVariable, BankAccount, TransactionCategory


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['category_name', 'description']


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'date', 'account_balance']


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['transaction_type_name', 'description']


class TransactionPlannedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionPlanned
        fields = ['id', 'amount',
                  'payment_term', 'date_valid_from',
                  'date_valid_up_including', 'category',
                  'description', 'transaction_type']

    def validate(self, data):
        if data['transaction_type'].transaction_type_name not in ['income_planned', 'spending_planned']:
            raise serializers.ValidationError(
                {'transaction_type': 'Transaction type must be income_planned or spending_planned.'})

        return data


class TransactionVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionVariable
        fields = ['id', 'amount',
                  'date', 'category',
                  'description', 'transaction_type']

    def validate(self, data):
        if data['transaction_type'].transaction_type_name not in ['income_variable', 'spending_variable_planned', 'spending_variable_unplanned']:
            raise serializers.ValidationError(
                {'transaction_type': 'Transaction type must be income_variable, spending_variable_planned or spending_planned.'})

        return data
