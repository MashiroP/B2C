from django.contrib import admin
from .models import profile

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseAdmin

class PrifileInlien(admin.StackedInline):
    model = profile
    can_delete = False
class UserAdmin(BaseAdmin):
    inlines=(PrifileInlien,)
    list_display = ('username','name','email','is_staff','is_active','is_superuser')
    def name(self,obj):
        return obj.profile.name

    name.short_description='姓名'



admin.site.unregister(User)
admin.site.register(User,UserAdmin)

@admin.register(profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name')

# Register your models here.
