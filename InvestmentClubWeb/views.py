from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock
from django.contrib.auth.decorators import login_required

def index(request):
    latest_stock_list = Stock.objects.order_by('symbol')[:5]
    context = {
        'latest_stock_list': latest_stock_list,
    }
    return HttpResponse(render(request, 'club/index.html', context))

@login_required
def stocks(request):
    latest_stock_list = Stock.objects.order_by('symbol')[:5]
    context = {
        'latest_stock_list': latest_stock_list,
    }
    return HttpResponse(render(request, 'club/index.html', context))