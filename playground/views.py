from django.shortcuts import render
from django.http import HttpResponse
from cashflow.models import Cashflow

# Create your views here.
def say_hello(request):
    query_set = Cashflow.objects.all()

    for cashflow in query_set:
        print(cashflow)

    return render(request, 'hello.html')

