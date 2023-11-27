
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cashflow.pagination import DefaultPagination
from cashflow.models import TransactionType, TransactionPlanned, TransactionVariable, BankAccount, TransactionCategory
from cashflow.serializers import TransactionTypeSerializer, TransactionPlannedSerializer, TransactionVariableSerializer, BankAccountSerializer
from datetime import datetime
import pandas as pd
from json import loads
from .constants import payment_term_multipliers


class BankAccountViewSet(ModelViewSet):
    serializer_class = BankAccountSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = CashflowFilter
    search_fields = ['description']
    ordering_fields = ['id', 'amount']
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if BankAccount.objects.filter(id=kwargs['pk']).count() > 1:
            return Response({'error': 'BankAccount cannot be deleted'})
        return super().destroy(request, *args, **kwargs)


class TransactionPlannedViewSet(ModelViewSet):
    serializer_class = TransactionPlannedSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['description']
    ordering_fields = ['id', 'amount']
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TransactionPlanned.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if TransactionPlanned.objects.filter(id=kwargs['pk']).count() > 1:
            return Response({'error': 'TransactionPlanned cannot be deleted'})
        return super().destroy(request, *args, **kwargs)


class TransactionVariableViewSet(ModelViewSet):
    serializer_class = TransactionVariableSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = CashflowFilter
    search_fields = ['description']
    ordering_fields = ['id', 'amount']
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TransactionVariable.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if TransactionVariable.objects.filter(id=kwargs['pk']).count() > 1:
            return Response({'error': 'TransactionVariable cannot be deleted'})
        return super().destroy(request, *args, **kwargs)


class TransactionTypeList(ListAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer


class CalculationTransactionsView(ListAPIView):
    def queryset(self):
        return TransactionVariable.objects.none()  # Return an empty queryset

    def get(self, request, *args, **kwargs):
        user = self.request.user
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']

        # obtain variable transactions
        queryset_variable = TransactionVariable.objects.filter(
            user=user,
            date__range=(start_date, end_date)
        )
        df_variable = pd.DataFrame(TransactionVariableSerializer(
            queryset_variable, many=True).data)

        # obtain fixed transactions
        queryset_fixed = TransactionPlanned.objects.filter(
            user=user,
            date_valid_from__gte=start_date,
            date_valid_up_including__gte=start_date
        )
        df_fixed = pd.DataFrame(TransactionPlannedSerializer(
            queryset_fixed, many=True).data)

        df_fixed['yearly_amount'] = df_fixed.apply(
            lambda row: row['amount'] *
            payment_term_multipliers.get(row['payment_term'], pd.NA),
            axis=1
        )
        df_fixed['amount'] = df_fixed['yearly_amount'] / 365
        df_fixed['date_valid_from'] = pd.to_datetime(
            df_fixed['date_valid_from'])

        df_fixed['date_valid_up_including'] = pd.to_datetime(
            df_fixed['date_valid_up_including'])

        df_fixed['date'] = df_fixed.apply(
            lambda row: pd.date_range(
                start=row['date_valid_from'],
                end=row['date_valid_up_including'],
                freq='D'),
            axis=1
        )
        df_fixed = df_fixed[[
            'id',
            'transaction_type',
            'amount',
            'date']]
        df_fixed = df_fixed.explode('date')

        df_fixed['date'] = df_fixed['date'].dt.strftime('%Y-%m-%d')

        result_df = \
            pd.concat(
                [df_variable,
                 df_fixed],
                ignore_index=True)

        result_df = \
            result_df[
                (result_df['date'] >= start_date)
                & (result_df['date'] <= end_date)]
        result_df = \
            result_df.groupby(['transaction_type'])[
                'amount'].sum().reset_index()

        result_total = result_df['amount'].sum()
        available_budget_row = pd.DataFrame([{
            'transaction_type': 'available_budget',
            'amount': result_total
        }])
        result_df = pd.concat(
            [result_df, available_budget_row], ignore_index=True)

        transaction_types = [
            'income_planned',
            'income_variable',
            'spending_planned',
            'spending_variable_planned',
            'spending_variable_unplanned'
        ]
        default_values = {
            'transaction_type': transaction_types,
            'amount': 0
        }
        default_df = pd.DataFrame(default_values)
        missing_types = default_df[default_df['transaction_type'].isin(
            result_df['transaction_type']) == False]
        result_df = pd.concat([result_df, missing_types], ignore_index=True)
        result_df = loads(result_df.to_json(orient="records"))
        return Response(result_df)
