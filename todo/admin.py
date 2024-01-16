from django.contrib import admin
from .models import Task
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')
    # list_filter = ('is_staff', 'is_active')
    
class TaskAdmin(admin.ModelAdmin):
    list_display = ('owner','name', 'description', 'completed', 'created_at')

admin.site.register(CustomUser, CustomUserAdmin)


    
admin.site.register(Task , TaskAdmin)