from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('transaction-planned', views.TransactionPlannedViewSet,
                basename='transaction-planned')
router.register('transaction-variable', views.TransactionVariableViewSet,
                basename='transaction-variable')
router.register('bank-account', views.BankAccountViewSet,
                basename='bank-account')

urlpatterns = [
    path('transaction-types/', views.TransactionTypeList.as_view(),
         name='transaction-type-list'),
    path('calculations/transactions/<str:start_date>/<str:end_date>/',
         views.CalculationTransactionsView.as_view(), name='calculation_transactions'),
]

urlpatterns += router.urls
