import datetime

import unicodedata
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomLoginForm
from .models import Card, Base, Company


# Create your views here.
@login_required(login_url="/login")
def nav(request):
    return render(request, 'nav.html')


@login_required(login_url="/login")
def orders(request):
    return render(request, 'Orders - ElonMoney Shop.html')


@login_required(login_url="/login")
def topup(request):
    return render(request, 'Topup - ElonMoney Shop.html')


@login_required(login_url="/login")
def cardstore(request):
    return render(request, 'Purchase Cards - ElonMoney Shop.html', context={"cards": Card.objects.all()[0:50],
                                                                            "companies": Company.objects.all(),
                                                                            "bases": Base.objects.all()})


@login_required(login_url="/login")
def dynamic_topics(request):
    return render(request, 'Dynamic Topups - ElonMoney Shop.html')


@login_required(login_url="/login")
def head(request):
    return render(request, 'header.html')


@login_required(login_url="/login")
def index(request):
    print(request.user)
    return render(request, 'Dashboard - ElonMoney Shop.html', context={"user": request.user})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(1)
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('/')  # Redirect to the home page or dashboard
    else:
        form = CustomUserCreationForm()

    return render(request, 'Create an Account - ElonMoney Shop.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'Login - ElonMoney Shop.html'
    form_class = CustomLoginForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('index')


def logout(request):
    auth.logout(request)
    return redirect('login')


def remove_accents(input_str):
    return ''.join(c for c in unicodedata.normalize('NFKD', input_str) if unicodedata.category(c) != 'Mn')


def search_card_page(request):
    # Извлечение параметров из GET-запроса
    ifis = request.GET.get('ifis', '')
    page = request.GET.get('page', '')
    bin_value = remove_accents(request.GET.get('bin', ''))
    base_name = request.GET.get('base', '')
    expired = request.GET.get('expired', '')
    city = remove_accents(request.GET.get('city', ''))
    state = remove_accents(request.GET.get('state', ''))
    zip_code = remove_accents(request.GET.get('zip', ''))
    country_name = remove_accents(request.GET.get('country', ''))
    company_name = request.GET.get('company', '')
    month = 1
    year = 1
    # Парсинг даты, если поле expired передано
    if expired:
        try:
            month, year = map(int, expired.split('/'))
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use MM/YYYY.'}, status=400)

    # Фильтрация карт
    print(page)
    services_per_page = 2
    start = (int(page) - 1) * services_per_page
    end = start + services_per_page
    print(start, end)
    exist = False

    try:
        if ifis:
            cards = Card.objects.all()
        else:
            cards = Card.objects.filter(
                city__icontains=city,
                BIN__icontains=bin_value,
                state__icontains=state,
                ZIP_code__icontains=zip_code,
                Company__name=company_name,
                country__name=country_name,
                Base__name=base_name,
                expired__year=year,
                expired__month=month
            )
        exist = len(cards) > end

    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company not found.'}, status=404)
    except Base.DoesNotExist:
        return JsonResponse({'error': 'Base not found.'}, status=404)
    a = []
    for i in cards[start:end]:
        a.append({"BIN": i.BIN,
                  "Base": i.Base.name,
                  "expired": i.expired,
                  'city': i.city,
                  'state': i.state,
                  "ZIP_code": i.ZIP_code,
                  "country": i.country,
                  "Company": i.Company.name,
                  "price": i.price,
                  "bank": i.bank,
                  "exists_next": exist})
    # Логирование данных
    print(a)
    print(bin_value, base_name, expired, city, state, zip_code, country_name, company_name)

    # Возвращаем JSON-ответ с данными
    return JsonResponse(a, safe=False)
