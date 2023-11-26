
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cashflow.pagination import DefaultPagination
from cashflow.models import TransactionType, TransactionPlanned, TransactionVariable, BankAccount
from cashflow.serializers import TransactionTypeSerializer, TransactionPlannedSerializer, TransactionVariableSerializer, BankAccountSerializer


class BankAccountViewSet(ModelViewSet):
    serializer_class = BankAccountSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = CashflowFilter
    search_fields = ['description']
    ordering_fields = ['id', 'amount']
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BankAccount.objects.all()

        return BankAccount.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if BankAccount.objects.filter(id=kwargs['pk']).count() > 1:
            return Response({'error': 'BankAccount cannot be deleted'})

        return super().destroy(request, *args, **kwargs)


class TransactionPlannedViewSet(ModelViewSet):
    serializer_class = TransactionPlannedSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_class = CashflowFilter
    search_fields = ['description']
    ordering_fields = ['id', 'amount']
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TransactionPlanned.objects.all()

        return TransactionPlanned.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if TransactionPlanned.objects.filter(id=kwargs['pk']).count() > 0:
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
        user = self.request.user
        if user.is_staff:
            return TransactionVariable.objects.all()

        return TransactionVariable.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if TransactionVariable.objects.filter(id=kwargs['pk']).count() > 0:
            return Response({'error': 'TransactionVariable cannot be deleted'})

        return super().destroy(request, *args, **kwargs)


class TransactionTypeList(ListAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
