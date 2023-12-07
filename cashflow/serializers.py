from decimal import Decimal
from rest_framework import serializers
from .models import TransactionPlanned, TransactionVariable, BankAccount, TransactionCategory, TransactionPaymentTerm


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['id', 'category_name', 'description']


class TransactionPaymentTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionPaymentTerm
        fields = ['id',  'payment_term_name_dutch']


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'date', 'account_balance']


class TransactionPlannedSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.category_name', read_only=True)
    payment_term_name_dutch = serializers.CharField(
        source='payment_term.payment_term_name_dutch', read_only=True)

    class Meta:
        model = TransactionPlanned
        fields = ['id', 'amount',
                  'payment_term', 'payment_term_name_dutch', 'date_valid_from',
                  'date_valid_up_including', 'category', 'category_name',
                  'description']


class TransactionVariableSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.category_name', read_only=True)

    class Meta:
        model = TransactionVariable
        fields = ['id', 'amount',
                  'date', 'category', 'category_name',
                  'description']
