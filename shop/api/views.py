from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from api import forms


# Create your views here.
def nav(request):
    return render(request, 'nav.html')


def orders(request):
    return render(request, 'Orders - ElonMoney Shop.html')


def topup(request):
    return render(request, 'Topup - ElonMoney Shop.html')


def cardstore(request):
    return render(request, 'Purchase Cards - ElonMoney Shop.html')


def dynamic_topics(request):
    return render(request, 'Dynamic Topups - ElonMoney Shop.html')


def head(request):
    return render(request, 'header.html')


def index(request):
    return render(request, 'Dashboard - ElonMoney Shop.html')


