from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, View, ListView, UpdateView
from django.db import connection
from deploy_app.models import HostList
from . import forms
import os


class IndexView(TemplateView):
    template_name = 'index.html'


class HostListView(ListView):
    model = HostList
    template_name = 'HostList.html'
    context_object_name = "hostlist"

    def get_context_data(self, *, object_list=None, **kwargs):
        form = forms.HostListForm()
        context = super().get_context_data(**kwargs)
        context['form'] = form

        return context



class HostListUpdateView(UpdateView):
    model = HostList
    template_name = 'HostList.html'

    def get_object(self, queryset=None):
        edits = HostList.objects.get(id=self.kwargs['id'])
        return edits



class AddHostList(HostListView, View):

    def post(self, request, *args, **kwargs):
        cursor = connection.cursor()
        form = forms.HostListForm(request.POST)
        if form.is_valid():
            form.save()
            cursor.execute("SET @i=0;")
            cursor.execute("UPDATE `deploy_app_hostlist` SET `id`=(@i:=@i+1);")
            cursor.execute("ALTER TABLE `deploy_app_hostlist` AUTO_INCREMENT=0;")
            return redirect("/#hostlist")
        else:
            print(form.errors)
            return HttpResponse("数据有误")
        # host_name = request.POST.get("host_name", None)
        # ip = request.POST.get("ip_add", None)
        # domain = request.POST.get("domain", None)
        # username = request.POST.get("username", None)
        # password = request.POST.get("password", None)
        # port = request.POST.get("port", None)
        # key_file = request.FILES.get("key_file")
        # key_path = None
        # if key_file != None:
        #     if os.path.exists('./key_file'):
        #         key_path = './key_file/' + key_file.name
        #         with open('./key_file/' + key_file.name, 'wb') as f:
        #             for chunk in key_file:
        #                 f.write(chunk)
        #     else:
        #         os.mkdir('./key_file')
        # hostlist = HostList(host_name=host_name, host_ip=ip, domain=domain, host_user=username, host_password=password,
        #                     host_port=port, host_key_file=key_path)
        # hostlist.save()



def Dashboard(request):
    return render(request, 'Dashboard.html')


def Deploy(request):
    return render(request, 'Deploy.html')


def Install(request):
    return render(request, 'Install.html')


def Monitor(request):
    return render(request, 'Monitor.html')


def Site(request):
    return render(request, 'Site.html')
