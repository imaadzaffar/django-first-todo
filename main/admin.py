from django.contrib import admin
from .models import Item, TodoList

# Register your models here.
admin.site.register(TodoList)
admin.site.register(Item)
