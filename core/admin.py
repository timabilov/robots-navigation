from django.contrib import admin

# Register your models here.
from core.models import Route, Landmark

admin.site.register(Route)
admin.site.register(Landmark)