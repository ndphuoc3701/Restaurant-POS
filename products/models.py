# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# from datetime import datetime
from django.utils import timezone
import pytz


class Pos():
    @staticmethod
    def order(id_cus, id_place, note, list_food):
        for food in list_food:
            if not Food.objects.get(id=food['id']).check_available(food['size'], food['num']):
                return Food.objects.get(id=food['id']).name
        Order.create_order(id_cus=id_cus, id_place=id_place,
                           note=note)
        order = Order.objects.get(id=Order.objects.count())
        for food in list_food:

            food_id = Food.objects.get(id=food['id'])
            Food_Order.objects.create(
                id_food=food_id, id_order=order, size=food['size'], quantity=food['num'])
            food_id.update_food(food['size'], food['num'])
        return True

    @staticmethod
    def place_manage():
        return Place.objects.all()

    @staticmethod
    def check_reserved():
        return Place.objects.filter(status=2)

    @staticmethod
    def take_place(id_place):
        Place.objects.get(id=id_place).update_place(True)
        pass

    @staticmethod
    def cus_info():
        return Customer.objects.all()

    @staticmethod
    def order_history():
        return Order.objects.all()

    @staticmethod
    def print_order(id_order):
        return Order.objects.get(id=id_order)

    @staticmethod
    def pay(phone):
        cus = Customer.objects.get(phone=phone)
        order = Order.objects.filter(id_cus=cus)
        order = order[order.count()-1]
        return cus, order

    def confirm_pay(phone):
        cus, order = Pos.pay(phone)
        order.id_place.update_place(False)
        order.update_order(order.get_order_price())
        cus.update_cus(order.get_order_price())

    @staticmethod
    def feedback(phone, eval, comt):
        cus = Customer.objects.get(phone=phone)
        order = Order.objects.filter(id_cus=cus)
        order = order[order.count()-1]
        Feedback.objects.create(
            id_cus=cus, id_order=order, evaluate=evaluate, comment=comt)


class Customer(models.Model):

    name = models.CharField(max_length=10)
    phone = models.IntegerField(unique=True, blank=False, null=False)
    email = models.CharField(
        db_column='Email', max_length=20, blank=True, null=True)

    level = models.CharField(
        db_column='Level', max_length=8, blank=True, default='Đồng')

    totalorder = models.IntegerField(
        db_column='TotalOrder', blank=True, default=0)

    totalpay = models.IntegerField(db_column='TotalPay', blank=True, default=0)

    def update_cus(self, price):
        self.totalorder += 1
        self.totalpay += price
        if self.totalpay > 5000:
            self.level = 'Vàng'
        elif self.totalpay > 2000:
            self.level = 'Bạc'
        super().save()


class Feedback(models.Model):

    id_cus = models.ForeignKey(Customer, on_delete=models.CASCADE)

    id_order = models.ForeignKey('Order', on_delete=models.CASCADE)

    evaluate = models.IntegerField(blank=False, null=False)

    comment = models.CharField(
        db_column='Comment', max_length=20, blank=True, null=True)

    @staticmethod
    def create_feedback():
        Feedback


class Food(models.Model):

    name = models.CharField(db_column='Name', unique=True,
                            max_length=10, blank=False, null=False)

    num_size = models.IntegerField(db_column='Num_Size', blank=True, default=1)

    remain = models.FloatField(default=100)

    price = models.IntegerField(db_column='Price', blank=False, null=False)
    image = models.ImageField(null=True, blank=True)

    def check_available(self, size, quantity):
        if size*quantity > self.remain:
            return False
        return True

    def update_food(self, size, quantity):
        self.remain = self.remain-size*quantity
        super().save()


class Food_Order(models.Model):

    id_food = models.ForeignKey(Food, on_delete=models.CASCADE)

    id_order = models.ForeignKey('Order', on_delete=models.CASCADE)

    size = models.IntegerField(blank=True, default=1)

    quantity = models.IntegerField(blank=True, default=1)

    class Meta:
        unique_together = (('id_food', 'id_order'),)

    @property
    def get_price(self):
        return Food.objects.get(id=self.id_food.id).price*self.size*self.quantity


class Order(models.Model):

    id_cus = models.ForeignKey(Customer, on_delete=models.CASCADE)

    id_place = models.ForeignKey(
        'Place', on_delete=models.CASCADE, related_name='order')

    starttime = models.DateTimeField(blank=True, auto_now_add=True)

    endtime = models.DateTimeField(blank=True, null=True)

    note = models.CharField(max_length=20, blank=True, null=True)

    status = models.IntegerField(blank=True, default=0)

    totalprice = models.IntegerField(blank=True, default=0)

    @staticmethod
    def create_order(id_cus, id_place, note):
        cus = Customer.objects.get(id=id_cus)
        place = Place.objects.get(id=id_place)
        Order.objects.create(id_cus=cus, id_place=place, note=note)

    def update_order(self, price):
        self.totalprice += price
        self.status = 1
        self.endtime = timezone.now()
        super().save()

    def get_order_price(self):
        a = Food_Order.objects.filter(id_order=self)
        price = 0
        for i in a:
            price += i.get_price
        return price

    def get_order_item(self):
        return Food_Order.objects.filter(id_order=self)


class Place(models.Model):

    status = models.IntegerField(blank=True, default=0)
    reserve = models.OneToOneField(
        Customer, blank=True, null=True, on_delete=models.CASCADE)

    def update_place(self, a: bool):
        if not a:
            self.status = 0
            self.reserve = None
        else:
            self.status = 1
        # super().save()


class Staff(models.Model):

    name = models.CharField(max_length=10, blank=True, null=True)

    username = models.CharField(unique=True, max_length=10)

    password = models.CharField(max_length=10, blank=False, null=False)

    @staticmethod
    def request_place():
        return Pos.place_manage()

    @staticmethod
    def request_order(id_cus, id_place, note, list_food):
        return Pos.order(id_cus, id_place, note, list_food)

    @staticmethod
    def request_pay(phone):
        return Pos.pay(phone)
