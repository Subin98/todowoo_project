from django.contrib import admin
from .models import todo

#restrit edit access of user userField

class todoadmin(admin.ModelAdmin):
    readonly_fields=('created',)

    # Register your models here.
admin.site.register(todo, todoadmin)
