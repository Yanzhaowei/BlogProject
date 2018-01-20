from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Ad)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Tag)
admin.site.register(User)