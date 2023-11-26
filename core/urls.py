from django.urls import path
from .views import CustomUserDeleteView

urlpatterns = [
    path('user/delete-account/', CustomUserDeleteView.as_view(), name='user-delete'),
]
