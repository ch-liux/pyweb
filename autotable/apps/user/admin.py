from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = '后台管理'
admin.site.site_title = '后台管理'
admin.site.index_title = ''
