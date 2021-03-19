from django.contrib import admin
from .models import User, Resturant, Info, Comment


# Register your models here.
admin.site.register(User)
admin.site.register(Resturant)
admin.site.register(Info)
admin.site.register(Comment)