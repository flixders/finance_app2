from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSet, TransactionPlannedViewSet, TransactionVariableViewSet, TransactionTypeList, TransactionCategoryList, CalculationBudgetView, CalculationSpendingVariableView, CalculationSpendingVariableIntervalView

router = DefaultRouter()
router.register(r'bank-account', BankAccountViewSet, basename='bank-account')
router.register(r'transaction-planned', TransactionPlannedViewSet,
                basename='transaction-planned')
router.register(r'transaction-variable', TransactionVariableViewSet,
                basename='transaction-variable')

urlpatterns = [
    path('', include(router.urls)),
    path('transaction-type-list/', TransactionTypeList.as_view(),
         name='transaction-type-list'),
    path('transaction-category-list/', TransactionCategoryList.as_view(),
         name='transaction-category-list'),
    path('calculations/budget/<str:start_date>/<str:end_date>/',
         CalculationBudgetView.as_view(), name='calculate-budget'),
    path('calculations/spending-variable/<str:start_date>/<str:end_date>/',
         CalculationSpendingVariableView.as_view(), name='calculate-spending-variable'),
    path('calculations/spending-variable-interval/<str:start_date>/<str:end_date>/<int:interval>',
         CalculationSpendingVariableIntervalView.as_view(), name='calculate-spending-variable'),
]
