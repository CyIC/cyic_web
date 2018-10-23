from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock, Profile
from django.contrib.auth.models import User
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
    print(context)
    return HttpResponse(render(request, 'club/stock.html', context))


def teampage(request):
    return HttpResponse(render(request, 'club/teampage.html'))

@login_required
def reports(request):
    context = {
        'latest_stock_list': {}
    }
    return HttpResponse(render(request, 'club/reports.html'), context)

@login_required
def dues(request):
    admin_user = User.objects.filter(username='admin')
    all_members = Profile.objects.all().exclude(user__username='admin')
    for x in all_members:
        all_units = 5
    context = {
        'members_list': all_members,

    }
    return HttpResponse(render(request, 'club/dues.html', context))
