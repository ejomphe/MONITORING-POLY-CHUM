from django.contrib import admin
from .models import Salle, Boitier, Montage
# Register your models here.


class BoitierInline(admin.StackedInline):
    model = Boitier
    extra = 0
    show_change_link = True


class MontageInline(admin.StackedInline):
    model = Montage
    extra = 0


class SalleAdmin(admin.ModelAdmin):
    inlines = [
        BoitierInline

    ]


class BoitierAdmin(admin.ModelAdmin):
    inlines = [
        MontageInline
    ]


admin.site.register(Salle, SalleAdmin)
admin.site.register(Boitier, BoitierAdmin)
admin.site.register(Montage)
