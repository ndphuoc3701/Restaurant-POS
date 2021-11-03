from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.forms.models import model_to_dict
from django.http import JsonResponse
# Create your views here.
cus = ''
place = ''


def home(request):

    # return render(request, "home.html", {})
    return render(request, "t/menu.html", {'type': 100})


def cus_list(request):

    rec = Pos.cus_info()
    context = {"cus_list": rec, 'type': 106}
    # return render(request, "product/cus_list.html", context)
    return render(request, "t/menu.html", context)


def print_cus_info(request, id):
    rec = Customer.objects.get(id=id)
    context = {"item": rec, 'type': 106}
    # return render(request, "product/cus_info.html", context)
    return render(request, "t/menu.html", context)


def order_history(request):
    context = {"type": 103, "order_history": Pos.order_history()}
    # return render(request, "product/order_history.html", context)
    return render(request, "t/menu.html", context)


def print_order(request, id):
    a = Pos.print_order(id)
    order = Order.objects.all()[id-1]
    context = {"type": 109, "order": order,
               "items": a.get_order_item(), 'price': a.get_order_price()}
    # return render(request, "product/print_order.html", context)
    return render(request, "t/menu.html", context)


def place_list(request):
    rec = Staff.request_place()
    context = {"place": rec}
    return render(request, "product/place_list.html", context)


def reservation(request):
    rec = Pos.check_reserved()
    context = {"reservation": rec, "id_order": Order.objects.count()+1}
    return render(request, "product/reservation.html", context)


def get_cus_info(request, id):
    if request.method == "POST":
        cus_name = request.POST.get('name')
        cus_phone = request.POST.get('phone')
        cus_email = request.POST.get('email')
        global cus, place
        try:
            cus = Customer.objects.get(phone=cus_phone)
            cus = model_to_dict(cus)['id']
        except:
            cus = Customer.objects.create(
                name=cus_name, phone=cus_phone, email=cus_email)

        place = id
        Pos.take_place(id)
        return redirect("product:create-order", id=Order.objects.count()+1)
    return render(request, "product/input_cus.html", {})


def create_order(request, id):
    # rec = Food.objects.all()[0:8]
    category = {}
    category['main_food'] = Food.objects.all()[0:8]
    category['drink'] = Food.objects.all()[8:16]
    category['fast_food'] = Food.objects.all()[16:24]
    context = {"food_list": category, 'id_order': id, 'type': 101}
    # return render(request, "product/food_add.html", context)
    return render(request, "t/menu.html", context)

# Thiếu note


def check_order(request, id):
    import json
    a = json.loads(request.body)
    global cus, place
    x=Staff.request_order(cus, place, 'note', a)
    return JsonResponse(True, safe=False) if x == True else JsonResponse(x, safe=False)


def confirm_reserve(request):
    import json
    a = json.loads(request.body)
    global cus, place
    cus = a['id_cus']
    place = a['id_place']
    Pos.take_place(place)
    return JsonResponse(True, safe=False)


def pay(request):
    return render(request, "product/pay.html", {})


def pay_fetch(request):
    import json
    a = json.loads(request.body)
    phone = a['phone']
    cus, order = Staff.request_pay(phone)
    return JsonResponse(order.get_order_price(), safe=False)


def pay_confirm(request):
    import json
    a = json.loads(request.body)
    phone = a['phone']
    Pos.confirm_pay(phone)
    return JsonResponse(None, safe=False)
