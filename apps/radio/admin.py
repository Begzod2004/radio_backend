from django.contrib import admin
from .models import *
#  Register your models here.'
from django.contrib import admin
from parler.admin import TranslatableAdmin





class ProgramAdmin(TranslatableAdmin):
    list_display = ['title']
 


admin.site.register(Music)
list_display = ['title', 'artiste']
admin.site.register(Program,ProgramAdmin)
