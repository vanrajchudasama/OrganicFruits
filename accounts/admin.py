from django.contrib import admin
from django.db import models
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from .widgets import ButtonWidget

admin.site.site_header = 'Shop Admin Dashbord'
class CustomUserAdmin(UserAdmin):
    using = 'mysql'
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','full_name','gender','mobile','image_tag', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    
    fieldsets = (
        (None, {'fields': ('first_name','last_name','gender','dob','email','mobile', 'password','profile')}),
        (_('Permissions'), {'fields': (('is_varified','is_active', 'is_staff', 'is_superuser'),
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide','extrapretty'),
            'fields': (('first_name','last_name'),('gender','dob'),('email','mobile'), ('password1', 'password2'),('profile'))}
        ),
        (_('Permissions'), {'fields': (('is_varified','is_active', 'is_staff', 'is_superuser'),
                                       'groups', 'user_permissions')}),
    )
   
    search_fields = ('email',)
    ordering = ('email',)
    
    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using='default')
        obj.save(using='mysql')
    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)
        obj.delete(using='default')

    # def get_queryset(self, request):
    #     # Tell Django to look for objects on the 'other' database.
    #     return super().get_queryset(request).using('default')
    #     return super().get_queryset(request).using(self.using)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     # Tell Django to populate ForeignKey widgets using a query
    #     # on the 'other' database.
    #     return super().formfield_for_foreignkey(db_field, request, using='default', **kwargs)
    #     return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     # Tell Django to populate ManyToMany widgets using a query
    #     # on the 'other' database.
    #     return super().formfield_for_manytomany(db_field, request, using='default', **kwargs)
    #     return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


admin.site.register(CustomUser, CustomUserAdmin)