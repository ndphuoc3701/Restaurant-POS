from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Place)
admin.site.register(Food)
admin.site.register(Food_Order)
admin.site.register(Order)
admin.site.register(Feedback)
