from django.contrib import admin
from .models import Member, Staff


class MemberAdmin(admin.ModelAdmin):
    list_display = ('username')


admin.site.register(Member,MemberAdmin)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('username')


admin.site.register(Staff, StaffAdmin)