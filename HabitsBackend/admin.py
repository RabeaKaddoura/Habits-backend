from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Counter, Reward
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Counter)
admin.site.register(Reward)