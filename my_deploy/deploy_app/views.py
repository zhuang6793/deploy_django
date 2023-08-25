import os
import paramiko
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from . import forms
from .models import HostList, InstallServer

cur_path = os.path.dirname(os.path.realpath(__file__))


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'index/index.html'


class HostListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = HostList
    template_name = 'client/list.html'
    context_object_name = "hostlist"

    def get_context_data(self, *, object_list=None, **kwargs):
        form = forms.HostListForm()
        context = super().get_context_data(**kwargs)
        context['hostlist'] = self.object_list.filter(is_active=True)
        context['form'] = form
        return context


class DelHostList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = 'polls.can_vote'

    def post(self, request):
        data = request.POST
        try:
            list = HostList.objects.filter(id=data['id'])
            list.delete()
            return HttpResponse('{"status": "true", "msg": "删除成功"}', content_type="application/json")
        except Exception as e:
            return HttpResponse('{"status": "false", "msg": "%s"}' % e, content_type="application/json")


class EditHostList(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    template_name = 'client/edit.html'
    form_class = forms.HostListForm
    permission_required = 'polls.can_vote'

    def get(self, request):
        id = request.GET.get('id')
        list = HostList.objects.get(id=id)
        return render(request, self.template_name, {'list': list})

    def post(self, request, *args, **kwargs):
        list = HostList.objects.get(id=request.POST.get('id'))
        form = self.form_class(request.POST, request.FILES, instance=list)
        if form.is_valid():
            form.save()
            return HttpResponse('{"status": "true", "msg": "修改成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "false", "msg": "修改失败"}', content_type="application/json")


class HostTestConnectView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        form = forms.HostListForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data['host_ip']
            username = form.cleaned_data['host_user']
            password = form.cleaned_data['host_password']
            port = form.cleaned_data['host_port']
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ip, port, username=username, password=password, timeout=1)
                return HttpResponse('{"status": "success",  "msg": "连接成功"}', content_type="application/json")
            except Exception as e:
                print(e)
                return HttpResponse('{"status": "failure", "msg": "连接失败"}', content_type="application/json")
        return HttpResponse(form.is_valid())


class HostListUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = HostList
    form_class = forms.HostListForm
    template_name = 'UpdateHostList.html'
    success_url = reverse_lazy('deploy_app:hostList')

    # def get(self, request, *args, **kwargs):
    #     get_id = self.kwargs['pk']
    #     adv_positin = HostList.objects.get(id=get_id)
    #     form = self.form_class(instance=adv_positin)
    #     #return render(request, 'UpdateHostList.html', {'form': form, 'id': self.kwargs['pk']})
    #     return render(request, 'UpdateHostList.html', locals())


# class DeleteHostListView(DeleteView):
#     model = HostList
#     success_url = reverse_lazy('deploy_app:hostList')

class DeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        host_id = request.GET.get('host_id')
        if not host_id:
            return HttpResponse('----请求异常')
        try:
            h1 = HostList.objects.get(id=host_id)
        except Exception as e:
            print('------delete hostlist get error %s' % (e))
            return HttpResponse('----The hostlist id is error')
        h1.is_active = False
        h1.save()
        return HttpResponseRedirect('/hostlist')


class InstallView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = InstallServer
    template_name = 'Install.html'
    context_object_name = 'hoststatus'

    def get_queryset(self):
        hoststatus = InstallServer.objects.filter().all()
        # for i in hoststatus.get():
        #     try:
        #         client = paramiko.SSHClient()
        #         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #         client.connect(i.host_ip, i.host_port, username=i.host_user, password=i.host_password, timeout=1)
        #     except Exception as e:
        #         print(e)
        # return hoststatus
        print(hoststatus.get())




class get_service_status(View):
    def post(self, request, *args, **kwargs):
        pass


def Monitor(request):
    return render(request, 'Monitor.html')


def Site(request):
    return render(request, 'Site.html')


def Bootstrap(request):
    return render(request, 'public/layout.html')
