import json
from decimal import Decimal, InvalidOperation
import secrets
import string
import unicodedata
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm, CustomLoginForm
from .models import Card, Payment, ApiUser
from .utils import create_payment_address


@login_required(login_url="/login")
def nav(request):
    return render(request, 'nav.html')


@login_required(login_url="/login")
def orders(request):
    cards = []
    for i in Card.objects.all().filter(purchased_user=request.user):
        print(i)
        num = i.card_number
        cards.append({
            "id": i.id,
            "card_number": " ".join(num[i:i + 4] for i in range(0, len(num), 4)),
            "price": i.price,
            "Company": i.issuingnetwork,
            "expired": i.expired,
            "CVV": i.CVV,
            'country': i.country,
            'name': i.name,
            'bank': i.bank,
            'address': i.address,
        })
    return render(request, 'Orders - ElonMoney Shop.html',
                  context={"orders": cards})


@login_required(login_url="/login")
def topup(request):
    return render(request, 'Topup - ElonMoney Shop.html')


@login_required(login_url="/login")
def cardstore(request):
    return render(request, 'Purchase Cards - ElonMoney Shop.html', context={"cards": Card.objects.all()[0:50]})


def generate_secure_code(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


@login_required(login_url="/login")
def dynamic_topics(request):
    return render(request, 'Dynamic Topups - ElonMoney Shop.html',
                  context={'orders': Payment.objects.all().filter(client=request.user)})


@login_required(login_url="/login")
def head(request):
    return render(request, 'header.html', context={"balance": request.user.balance})


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
    ifis = request.GET.get('ifis', bool)
    page = request.GET.get('page', '')
    expired = request.GET.get('expired', '')
    country_name = remove_accents(request.GET.get('country', ''))
    company_name = request.GET.get('company', '')
    bank_name = request.GET.get('bank', '')

    print(page)
    services_per_page = 10
    start = (int(page) - 1) * services_per_page
    end = start + services_per_page
    print(start, end)
    exist = False
    print(expired, country_name, company_name, bank_name, ifis)
    if ifis:
        cards = Card.objects.all().filter(purchased=False)
    else:
        cards = Card.objects.filter(
            issuingnetwork=company_name,
            country=country_name,
            expired=expired,
            bank=bank_name,
            purchased=False,
        )
    exist = len(cards) > end

    a = []
    for i in cards[start:end]:
        a.append({"network": i.issuingnetwork,
                  "expired": i.expired,
                  "country": i.country,
                  "price": i.price,
                  "bank": i.bank,
                  "exists_next": exist,
                  "id": i.id})
    # Логирование данных

    # Возвращаем JSON-ответ с данными
    return JsonResponse(a, safe=False)


@csrf_exempt  # Используйте это только для тестирования! На продакшене лучше оставить CSRF защиту.
def purchase(request):
    if request.method == "POST":
        try:
            # Извлекаем JSON-данные из тела запроса
            data = json.loads(request.body)
            id = data.get('id')  # Получаем id из переданных данных

            # Пытаемся получить объект Card
            card = Card.objects.get(id=id)
            user = request.user
            print(card)  # Здесь вы можете добавить свою логику обработки покупки
            if card.price <= request.user.balance:
                user.balance -= card.price
                card.purchased = True
                card.purchased_user = request.user
                card.save()
                user.save()
            else:
                return JsonResponse({"error": "Balance is not enough"}, status=404)
            # Возвращаем успешный ответ
            return JsonResponse({"success": "purchased"}, safe=False)
        except Card.DoesNotExist:
            return JsonResponse({"error": "Card not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def check_card(request):
    if request.method == 'POST':
        try:
            # Получаем данные карты из запроса
            data = json.loads(request.body)
            card_number = data.get('cardNumber')
            expiry_date = data.get('expiryDate')
            cvv = data.get('cvv')
            LN = data.get('lastName')
            FN = data.get('firstName')
            post = data.get('postcode')
            adr = data.get('address')
            TC = data.get('city')

            print(" ".join(card_number[i:i + 4] for i in range(0, len(card_number), 4)), expiry_date, cvv)

            if not all([card_number, expiry_date, cvv, LN, FN, post, adr, TC]):
                return JsonResponse({'error': 'Missing card data'}, status=400)

            card_exists = Card.objects.filter(
                purchased=True,
                CVV=int(cvv),
                expired=expiry_date,
                card_number=card_number
            ).exists()
            print(card_exists)
            if card_exists:
                code = generate_secure_code()
                return JsonResponse({'exists': True, "code": code})

            return JsonResponse({'exists': False})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def new_topup(request):
    payment_data = create_payment_address()
    print(payment_data)
    payment = Payment.objects.create(
        client=request.user,
        payment_address=payment_data["address"],
        invoice=payment_data["invoice"],
        payment_code=payment_data["payment_code"],
        amount=request.POST.get("amount", 0),
        value=request.POST.get("amount", 0),

    )

    return render(request, "transaction.html", {"payment": payment})


@csrf_exempt
def callback(request):
    data = request.POST
    invoice = data.get("invoice")
    print(data)
    if Payment.objects.all().get(invoice=invoice).status == 'confirmed':
        return JsonResponse({"invoice": invoice})
    else:
        # Найти платеж по invoice
        try:
            payment = Payment.objects.select_for_update().get(invoice=invoice)
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)

        # Проверка и преобразование суммы
        try:
            kurs = Decimal(data['ETHUSD_AVERAGE'])
            amount = Decimal(data['amount'])
            val = amount / Decimal('1000000000000000000')
        except (KeyError, InvalidOperation):
            return JsonResponse({"error": "Invalid data format"}, status=400)

        # Обновляем значения платежа
        payment.value = val
        payment.amount = val * kurs
        payment.status = "confirmed"  # Обновляем статус
        payment.save()  # Сохраняем изменения

        # Обновляем баланс пользователя
        user = payment.client  # Связь через ForeignKey
        user.balance += payment.amount
        user.save()  # Сохраняем изменения

        print(payment.value)
        print(payment.amount)
        print(user.balance)

        return JsonResponse({"invoice": invoice})
