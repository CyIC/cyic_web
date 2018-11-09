from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Stock, Profile, Ledger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import DuesForm
import datetime

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

def package_user_data():
    all_members = Profile.objects.all().exclude(user__username='admin')
    # TODO package up reports data to pass into report
    return all_members


@login_required
def reports(request):
    context = {
        'members_list': package_user_data(),
        'latest_stock_list': {},
    }
    return HttpResponse(render(request, 'club/reports.html'), context)

@login_required
def dues(request):
    # TODO package up reports data to pass into report
    if request.method == 'POST':
        form = DuesForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Get ledger
            ledger = Ledger.objects.all()[int(request.POST.get('credit_ledger'))-1]
            cash = Ledger.objects.get(name='cash')
            post.notes = 'Dues for {} on {}'.format(ledger, datetime.datetime.now().strftime("%B %d, %Y"))
            post.debit_ledger = cash
            post.debit_amount = request.POST.get('credit_amount')
            post.credit_ledger = ledger
            post.credit_amount = request.POST.get('credit_amount')
            post.save()
            return HttpResponseRedirect('reports')
    else:
        form = DuesForm()
    return render(request, 'club/dues.html', {'form': form, 'members_list': package_user_data()})
