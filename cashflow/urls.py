from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSet, TransactionPlannedViewSet, TransactionVariableViewSet, TransactionCategoryList, TransactionPaymentTermList, CalculationBudgetOverviewView, CalculationBudgetOverviewIntervalView, CalculationSpendingVariableView

router = DefaultRouter()
router.register(r'bank-account', BankAccountViewSet, basename='bank-account')
router.register(r'transaction-planned', TransactionPlannedViewSet,
                basename='transaction-planned')
router.register(r'transaction-variable', TransactionVariableViewSet,
                basename='transaction-variable')

urlpatterns = [
    path('', include(router.urls)),
    path('transaction-payment-term-list/', TransactionPaymentTermList.as_view(),
         name='transaction-payment-term-list'),
    path('transaction-category-list/', TransactionCategoryList.as_view(),
         name='transaction-category-list'),
    path('calculations/budget-overview/<str:start_date>/<str:end_date>/',
         CalculationBudgetOverviewView.as_view(), name='calculate-budget-overview'),
    path('calculations/budget-interval/<str:end_date>/<int:interval>',
         CalculationBudgetOverviewIntervalView.as_view(), name='calculate-budget-overview'),
    path('calculations/spending-variable/<str:start_date>/<str:end_date>/',
         CalculationSpendingVariableView.as_view(), name='calculate-spending-variable'),
]
