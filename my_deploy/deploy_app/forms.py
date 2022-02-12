from django.forms import ModelForm
from . import models
from django.forms import widgets as wdt


class HostListForm(ModelForm):
    class Meta:
        model = models.HostList
        fields = ('host_name', 'host_ip', 'domain', 'host_user', 'host_password', 'host_port', 'host_key_file')
        # labels = {
        #     'host_name': '主机名称',
        #     'host_ip': 'IP地址',
        #     'domain': '域名',
        #     'host_user': '用户名',
        #     'host_password': '密码',
        #     'host_port': '端口',
        #     'host_key_file': '密钥'
        # }
        widgets = {
            'host_name': wdt.TextInput(attrs={"class": "form-control"}),
            'host_ip': wdt.TextInput(attrs={"class": "form-control"}),
            'domain': wdt.TextInput(attrs={"class": "form-control"}),
            'host_user': wdt.TextInput(attrs={"class": "form-control"}),
            'host_password': wdt.PasswordInput(render_value=True, attrs={"class": "form-control"}),
            'host_port': wdt.TextInput(attrs={"class": "form-control"}),
            'host_key_file': wdt.FileInput(attrs={"class": "form-control"})
        }

        error_messages = {
            "host_name": {
                "required": "主机名不能为空"
            },
            "host_ip": {"required": "IP地址不能为空"},
            "host_user": {"required": "用户名不能为空"},
            "host_port": {"required": "端口不能为空"},
        }