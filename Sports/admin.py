from django.contrib import admin
from .models import Sport, Slot, SportSpecificSlot


class SportAdmin(admin.ModelAdmin):
    list_display = ('name')


admin.site.register(Sport,SportAdmin)


class SlotAdmin(admin.ModelAdmin):
    list_display = ('slot')


admin.site.register(Slot,SlotAdmin)


class SportSpecificSlotAdmin(admin.ModelAdmin):
    list_display = ('name','court','slot','available')


admin.site.register(SportSpecificSlot,SportSpecificSlotAdmin)