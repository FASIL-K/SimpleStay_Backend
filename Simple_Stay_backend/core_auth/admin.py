from django.contrib import admin
from .models import User, UserDetail, OwnerDetail
# Register your models here.
admin.site.register(User)
admin.site.register(UserDetail)
admin.site.register(OwnerDetail)