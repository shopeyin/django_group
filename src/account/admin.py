from django.contrib import admin
from django.contrib.auth.admin import  UserAdmin,GroupAdmin 
from django.contrib.auth.models import Group
from .models import MyUser,Team,Invitation



class CustomUserAdmin(UserAdmin):
    fieldsets = (
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff','is_admin','is_superuser',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)


class CustomGroupAdmin(GroupAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


admin.site.register(MyUser,CustomUserAdmin)
admin.site.register(Team, CustomGroupAdmin)
admin.site.register(Invitation)
# Register your models here.
