from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('cashflow', views.CashflowViewSet, basename='cashflow')

urlpatterns = [
    path('cashflow-type/', views.CashflowTypeList.as_view(),
         name='cashflow_type_list'),

]

urlpatterns += router.urls
