
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cashflow.pagination import DefaultPagination
from cashflow.models import TransactionPlanned, TransactionVariable, BankAccount, TransactionCategory, TransactionPaymentTerm
from cashflow.serializers import TransactionPlannedSerializer, TransactionVariableSerializer, BankAccountSerializer, TransactionCategorySerializer, TransactionPaymentTermSerializer
from .calculations import calculate_budget
import pandas as pd
from json import loads
import json


class BankAccountViewSet(ModelViewSet):
    serializer_class = BankAccountSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = CashflowFilter
    search_fields = ['description']
    ordering_fields = ['id']
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
        if serializer.is_valid():
            transaction = serializer.save(user=self.request.user)
            transaction.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if serializer.is_valid():
            transaction = serializer.save(user=self.request.user)
            transaction.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        if serializer.is_valid():
            transaction = serializer.save(user=self.request.user)
            transaction.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        if serializer.is_valid():
            transaction = serializer.save(user=self.request.user)
            transaction.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        if TransactionVariable.objects.filter(id=kwargs['pk']).count() > 1:
            return Response({'error': 'TransactionVariable cannot be deleted'})
        return super().destroy(request, *args, **kwargs)


class TransactionCategoryList(ListAPIView):
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer


class TransactionPaymentTermList(ListAPIView):
    queryset = TransactionPaymentTerm.objects.all()
    serializer_class = TransactionPaymentTermSerializer


class CalculationBudgetOverviewView(ListAPIView):
    def queryset(self):
        return TransactionVariable.objects.none()  # Return an empty queryset

    def get(self, request, *args, **kwargs):
        user = self.request.user
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']

        df = \
            calculate_budget(
                start_date=start_date,
                end_date=end_date,
                TransactionVariable=TransactionVariable,
                TransactionPlanned=TransactionPlanned,
                user=user)

        transaction_types = [
            'variable_spending',
            'fixed_income',
            'fixed_spending'
        ]
        default_values = {
            'transaction_type_name': transaction_types,
            'amount': 0
        }
        default_df = pd.DataFrame(default_values)
        missing_types = default_df[default_df['transaction_type_name'].isin(
            df['transaction_type_name']) == False]
        df = pd.concat([df, missing_types], ignore_index=True)
        df = loads(df.to_json(orient="records"))
        return Response(df)


class CalculationBudgetOverviewIntervalView(ListAPIView):
    def queryset(self):
        return TransactionVariable.objects.none()  # Return an empty queryset

    def get(self, request, *args, **kwargs):
        user = self.request.user
        end_date = self.kwargs['end_date']
        interval = self.kwargs['interval']

        end_date = pd.to_datetime(end_date).date()
        start_date = end_date - pd.Timedelta(days=10 * interval)
        start_date = pd.to_datetime(start_date).date()
        results = pd.DataFrame(
            columns=['transaction_type_name', 'amount', 'transaction_type_title', 'date'])
        resampling_freq = f"{interval}D"
        date_range = pd.date_range(
            start=start_date, end=end_date, freq=resampling_freq)

        # Iterate through the date range intervals and calculate budget for each interval (still buggy )
        for start, stop in zip(date_range[:-1], date_range[1:]):
            result_for_interval = calculate_budget(
                start_date=start,
                end_date=stop,
                TransactionVariable=TransactionVariable,
                TransactionPlanned=TransactionPlanned,
                user=user)
            result_for_interval['date'] = start
            results = pd.concat(
                [results, result_for_interval], ignore_index=True)

        df_result = pd.DataFrame(results)
        df_result['date'] = pd.to_datetime(
            df_result['date'], unit='ms').dt.strftime('%Y-%m-%d')
        df_result = loads(df_result.to_json(orient="records"))
        return Response(df_result)


class CalculationSpendingVariableView(ListAPIView):
    def queryset(self):
        return TransactionVariable.objects.none()  # Return an empty queryset

    def get(self, request, *args, **kwargs):
        user = self.request.user
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']
        start_date = pd.to_datetime(start_date).date()
        end_date = pd.to_datetime(end_date).date()

        # obtain variable transactions
        queryset_variable = TransactionVariable.objects.filter(
            user=user,
            date__range=(start_date, end_date)
        ).select_related('transaction_type')
        data_variable = list(queryset_variable.values(
            'amount',
            'date',
            category_name=F('category__category_name')))
        df_variable = pd.DataFrame(data_variable)
        result_df = df_variable.groupby('category_name')[
            'amount'].sum().reset_index()
        result_df = loads(result_df.to_json(orient="records"))
        return Response(result_df)
