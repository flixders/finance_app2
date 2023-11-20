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
         name='transaction-type-list')
]

urlpatterns += router.urls
