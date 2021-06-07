from django.contrib import admin
from deploy_app.models import *

class HostManager(admin.ModelAdmin):
    list_display = ['host_name', 'host_ip', 'host_user', 'host_port', 'host_key_file', 'domain', 'is_active']
    list_display_links = ['host_name']
    list_filter = ['host_name']
    search_fields = ['host_ip']
    list_editable = ['host_ip']
class TestManager(admin.ModelAdmin):
    list_display = ['id', 't1', 't2', 'num']


# Register your models here.
admin.site.register([HostList], HostManager)
admin.site.register(Test, TestManager)