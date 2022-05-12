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


class Pos:
    orde = ''

    @staticmethod
    def login(username, password):
        return StaffDB.check(username, password)

    @staticmethod
    def order(id_cus, id_place, note, list_food):
        for food in list_food:
            if not FoodDB.check_available(food['id'], food['size'], food['num']):
                return Food.objects.get(id=food['id']).name
        OrderDB.create_order(id_cus=id_cus, id_place=id_place,
                             note=note)
        order = Order.objects.all().last()
        for food in list_food:
            food_id = Food.objects.get(id=food['id'])
            Food_Order.objects.create(
                id_food=food_id, id_order=order, size=food['size'], quantity=food['num'])
            FoodDB.update_food(food_id, food['size'], food['num'])
        OrderDB.update_order(order, order.get_order_price())
        return True

    @staticmethod
    def place_manage():
        return PlaceDB.show_place()

    @staticmethod
    def check_reserved():
        return Place.objects.filter(status=2)

    @staticmethod
    def take_place(id_place):
        PlaceDB.update_place(id_place, True)

    @staticmethod
    def cus_list():
        return CustomerDB.get_cus_list()

    @staticmethod
    def cus_info(id):
        return CustomerDB.get_cus_info(id)

    @staticmethod
    def order_history():
        return OrderDB.get_order_history()

    @staticmethod
    def print_order(id_order):
        return OrderDB.get_order_info(id_order, True)

    @classmethod
    def pay(cls, phone):
        cus = Customer.objects.get(phone=phone)
        cls.orde = Order.objects.filter(id_cus=cus)
        cls.orde = cls.orde[cls.orde.count()-1]
        return cls.orde.get_order_item(), cus

    @classmethod
    def confirm_pay(cls):
        PlaceDB.update_place(cls.orde.id_place.id, False)
        OrderDB.update_order(cls.orde, 0)
        cls.orde.id_cus.update_cus(cls.orde.get_order_price())

    @classmethod
    def feedback(cls, eval, comt):
        FeedbackDB.create_feedback(cls.orde, eval, comt)


class CustomerDB:
    @staticmethod
    def get_cus_list():
        return Customer.objects.all()

    @staticmethod
    def get_cus_info(id):
        return Customer.objects.get(id=id)


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


class FeedbackDB:
    @staticmethod
    def create_feedback(order, eval, comt):
        Feedback.objects.create(id_order=order, evaluate=eval, comment=comt)


class Feedback(models.Model):

    id_order = models.OneToOneField(
        'Order', on_delete=models.CASCADE, unique=True)

    evaluate = models.IntegerField(blank=False, null=False)

    comment = models.CharField(
        db_column='Comment', max_length=20, blank=True, null=True)


class FoodDB:
    @staticmethod
    def check_available(id_food, size, num):
        return Food.objects.get(id=id_food).available(size, num)

    @staticmethod
    def update_food(food_id, size, quantity):
        food_id.update(size, quantity)


class Food(models.Model):

    name = models.CharField(db_column='Name', unique=True,
                            max_length=10, blank=False, null=False)

    num_size = models.IntegerField(db_column='Num_Size', blank=True, default=1)

    remain = models.FloatField(default=100)

    price = models.IntegerField(db_column='Price', blank=False, null=False)
    image = models.ImageField(null=True, blank=True)

    def available(self, size, quantity):
        if size*quantity > self.remain:
            return False
        return True

    def update(self, size, quantity):
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


class OrderDB:
    @staticmethod
    def create_order(id_cus, id_place, note):
        cus = Customer.objects.get(id=id_cus)
        place = Place.objects.get(id=id_place)
        Order.objects.create(id_cus=cus, id_place=place, note=note)

    @staticmethod
    def get_order_history():
        return Order.objects.all()

    @staticmethod
    def get_order_info(id_order, a: bool):
        return Order.objects.get(id=id_order)

    @staticmethod
    def update_order(order, price):
        order.update(price)


class Order(models.Model):

    id_cus = models.ForeignKey(Customer, on_delete=models.CASCADE)

    id_place = models.ForeignKey(
        'Place', on_delete=models.CASCADE, related_name='order')

    starttime = models.DateTimeField(blank=True, auto_now_add=True)

    endtime = models.DateTimeField(blank=True, null=True)

    note = models.CharField(max_length=20, blank=True, null=True)

    status = models.IntegerField(blank=True, default=0)

    totalprice = models.IntegerField(blank=True, default=0)

    def update(self, price):
        if price != 0:
            self.totalprice += price
        else:
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


class PlaceDB:
    @staticmethod
    def show_place():
        return Place.objects.all()

    @staticmethod
    def update_place(id_place, a: bool):
        Place.objects.get(id=id_place).update(a)


class Place(models.Model):

    status = models.IntegerField(blank=True, default=0)
    reserve = models.OneToOneField(
        Customer, blank=True, null=True, on_delete=models.CASCADE)

    def update(self, a: bool):
        if not a:
            self.status = 0
            self.reserve = None
        else:
            self.status = 1
        super().save()
