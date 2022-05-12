import django.contrib.auth
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate
from django.http import HttpResponse
# Create your views here.
cus = ''
place = ''


def home(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    return render(request, "t/home.html", {})


def cus_list(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    rec = Pos.cus_list()
    context = {"cus_list": rec, 'type': 106}
    return render(request, "t/Customer.html", context)


def print_cus_info(request, id):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    rec = Customer.objects.get(id=id)
    context = {"item": rec, 'type': 106}
    return render(request, "t/Customer Info.html", context)


def order_history(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    context = {"type": 103, "order_history": Pos.order_history()}
    return render(request, "t/Order.html", context)


def print_order(request, id):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    a = Pos.print_order(id)
    context = {"type": 301, "order": a,
               "items": a.get_order_item(), "order_history": Pos.order_history()}
    return render(request, "t/Order.html", context)


def place_list(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    rec = Pos.place_manage()
    context = {"place": rec}
    return render(request, "t/Table.html", context)


def reservation(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    rec = Pos.check_reserved()
    context = {"reservation": rec, "id_order": Order.objects.count()+1}
    return render(request, "t/Reservation.html", context)


def get_cus_info(request, id):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    if request.method == "POST":
        cus_name = request.POST.get('name')
        cus_phone = request.POST.get('phone')
        cus_email = request.POST.get('email')
        global cus, place
        try:
            cus = Customer.objects.get(phone=cus_phone)
        except:
            cus = Customer.objects.create(
                name=cus_name, phone=cus_phone, email=cus_email)
        place = id
        Pos.take_place(id)
        cus = model_to_dict(cus)['id']
        print(cus)
        return redirect("product:create-order", id=Order.objects.count()+1)
    return render(request, "t/Input Customer.html", {})


def create_order(request, id):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    category = {}
    category['main_food'] = Food.objects.all()[0:8]
    category['drink'] = Food.objects.all()[8:16]
    category['fast_food'] = Food.objects.all()[16:24]
    context = {"food_list": category, 'id_order': id, 'type': 101}
    return render(request, "t/Menu.html", context)


def check_order(request, id):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    import json
    a = json.loads(request.body)
    global cus, place
    try:
        print(cus, place)
        x = Pos.order(cus, place, '', a)
        return JsonResponse(True, safe=False) if x == True else JsonResponse(x, safe=False)
    except:
        return JsonResponse(False, safe=False)


def confirm_reserve(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    import json
    a = json.loads(request.body)
    global cus, place
    cus = Customer.objects.get(phone=a['id_cus'])
    cus = model_to_dict(cus)['id']
    place = a['id_place']
    Pos.take_place(place)
    return JsonResponse(True, safe=False)


def pay(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    return render(request, "t/Checkout.html", {})


def pay_fetch(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    import json
    a = json.loads(request.body)
    phone = a['phone']
    order, cus_pay = Pos.pay(phone)
    food = Food.objects.all()
    price = Pos.orde.get_order_price()
    qs_json = {}
    qs_json['cus'] = serializers.serialize('json', [cus_pay, ])
    qs_json['order'] = serializers.serialize('json', order)
    qs_json['food'] = serializers.serialize('json', food)
    return JsonResponse(qs_json, safe=False)


def pay_confirm(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    Pos.confirm_pay()
    return JsonResponse(None, safe=False)


def feedback(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    return render(request, "t/Feedback.html", {})


def feedback_confirm(request):
    if not request.user.is_authenticated:
        return render(request, "t/Login.html", {})
    import json
    a = json.loads(request.body)
    Pos.feedback(a['eval'], a['comt'])
    return JsonResponse(None, safe=False)


def login(request):
    if request.user.is_authenticated:
        return render(request, "t/home.html", {})
    return render(request, "t/Login.html", {})


def login_fetch(request):
    import json
    a = json.loads(request.body)
    userss = authenticate(username=a['user'], password=a['password'])
    if userss is not None:
        django.contrib.auth.login(request, userss)
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)


def logout(request):
    django.contrib.auth.logout(request)
    return render(request, "t/Login.html", {})
