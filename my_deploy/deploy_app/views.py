from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView
from django.db import connection
from .models import HostList, InstallServer

from django.core import serializers
from . import forms
import paramiko
import json


class IndexView(TemplateView):
    template_name = 'index/index.html'


class ClientListView(TemplateView):
    template_name = 'client/list.html'


class AddTempView(TemplateView, View):
    template_name = 'client/add.html'
    def get_context_data(self, **kwargs):
        form = forms.HostListForm()
        context = super(AddTempView, self).get_context_data(**kwargs)
        context['form'] = form
        return context


class GetClientListView(ClientListView, View):
    def post(self, request, *args, **kwargs):
        search = request.POST
        pageSize =  int(search.get('limit'))
        pageNumber = (int(search.get('offset')) / pageSize) + 1
        right_boundary = pageSize * pageNumber
        print(pageNumber, pageSize, right_boundary)
        print(type(HostList.objects.all()))
        articles = HostList.objects.all()[(pageNumber-1)*pageSize:right_boundary]
        total = HostList.objects.all().count()
        rows = []
        for article in articles:
            rows.append({'id': article.id, 'domain': article.domain, 'host_user': article.host_user, 'host_ip': article.host_ip, 'host_name': article.host_name, 'host_port': article.host_port})
        return JsonResponse({'code': 200, 'rows': rows, 'total': total})


class hostlist(View):
    def get(self, request, *args, **kwargs):
        list = HostList.objects.all()
        result_serialize = serializers.serialize('json', list)
        return HttpResponse(result_serialize, "application/json")


class HostListView(ListView):
    model = HostList
    template_name = 'client/list.html'
    context_object_name = "hostlist"

    def get_context_data(self, *, object_list=None, **kwargs):
        form = forms.HostListForm()
        context = super().get_context_data(**kwargs)
        context['hostlist'] = self.object_list.filter(is_active=True)
        context['form'] = form
        return context


class AddHostList(AddTempView, View):

    def post(self, request, *args, **kwargs):
        cursor = connection.cursor()
        form = forms.HostListForm(request.POST, request.FILES)
        if form.is_valid():
            cursor.execute("SET @i=0;")
            cursor.execute("UPDATE `deploy_app_hostlist` SET `id`=(@i:=@i+1);")
            cursor.execute("ALTER TABLE `deploy_app_hostlist` AUTO_INCREMENT=0;")
            form.save()
            return HttpResponse('{"status": "true", "msg": "添加成功"}', content_type="application/json")
        else:
            return HttpResponse(form.errors.as_json())

class DelHostList(View):
    def post(self, request):
        data = request.POST
        try:
            list = HostList.objects.filter(id = data['id'])
            list.delete()
            return HttpResponse('{"status": "true", "msg": "删除成功"}', content_type="application/json")
        except Exception as e:
            return HttpResponse('{"status": "false", "msg": "%s"}'%e, content_type="application/json")


class HostTestConnectView(View):

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



class HostListUpdateView(UpdateView):
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

class DeleteView(View):
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


def Dashboard(request):
    return render(request, 'Dashboard.html')


def asd(request):
    return render(request, 'asd.html')


def Deploy(request):
    return render(request, 'Deploy.html')


class InstallView(ListView):
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


def test1(request, y, m, d):
    print(request.COOKIES)
    print(request.session)
    print(request.body)
    print(request.scheme)
    print(request.path_info)
    print(request.get_full_path())
    print(request.META['REMOTE_ADDR'])

    return render(request, 'asd.html', {"y": y, "m": m, "d": d})


def HostConnect(ip, username, password, port):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port, username=username, password=password, timeout=1)
        return True
    except Exception as e:
        return False