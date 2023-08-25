from django.views.generic import TemplateView, View
from .client import GetClientListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .. import forms
from ..views import HostList
from django.shortcuts import render
import os
from ..tool import ssh_connect

cur_path = os.path.dirname(os.path.realpath(__file__))


class DeployListView(TemplateView, GetClientListView):
    template_name = 'client/deploy.html'


class ExecHost(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'client/exec.html'
    form_class = forms.HostListForm

    def get(self, request):
        id = request.GET.get('id')
        list = HostList.objects.get(id=id)
        return render(request, self.template_name, {'list': list})

    def post(self, request, *args, **kwargs):
        localpath = cur_path + '/deploy_file/'
        host = HostList.objects.get(id=request.POST.get('id'))
        file = request.FILES.getlist('web_file')
        plat = request.POST.get('option')
        if not os.path.exists(localpath):
            os.mkdir(localpath)
        print(file)
        if plat == '1':
            for f in file:
                host.get_ssh().put_file_by_fl(f, f'{host.des_path}/{f.name}')
        elif plat == '2':
            pass
        return HttpResponse('{"status": "true", "msg": "succes"}', content_type="application/json")
