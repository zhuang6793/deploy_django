import os
import platform
import subprocess

import paramiko
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, UpdateView

from . import forms
from .models import HostList, InstallServer

cur_path = os.path.dirname(os.path.realpath(__file__))


def server_status(ip_address):
    os_name = platform.system()

    if os_name == 'Windows':
        response = subprocess.Popen("ping -n 1 -w 100 %s " % ip_address, stdout=subprocess.PIPE)
    else:
        response = subprocess.Popen("ping -c 1 -w 100 %s" % ip_address, stdout=subprocess.PIPE)

    if response.wait() == 0:
        status = 'Online'
    else:
        status = 'Offline'

    return status


class SshUpload:
    def __init__(self, ip, port, user, passwd, filename, localpath, remotepath, deppath):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.filename = filename
        self.localpath = self._path(localpath)
        self.remotepath = self._path(remotepath)
        self.deppath = self._path(deppath)
        self.sshClient = self.ssh_client(self.ip, self.port, self.user, self.passwd)

    def ssh_client(self, ip, port, user, passwd):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, port=port, username=user, password=passwd)

        return client

    def _path(self, path):
        if path.split('/')[-1] != '':
            path = path + '/'

        return path

    def sftp_client(self):
        tran = paramiko.Transport((self.ip, int(self.port)))

        tran.connect(username=self.user, password=self.passwd)

        sftp = paramiko.SFTPClient.from_transport(tran)

        return sftp

    def run(self):
        self.sftp_client().put(localpath=self.localpath + self.filename, remotepath=self.remotepath + self.filename)

        stdin, stdout, stderr = self.sshClient.exec_command(
            f"sudo mv  {self.remotepath}{self.filename}  {self.deppath}{self.filename.split('.')[0]}  ")
        print(stdout.readline(), stderr.readline())
        stdin, stdout, stderr = self.sshClient.exec_command(
            f"cd  {self.deppath}{self.filename.split('.')[0]}  && sudo unzip -o {self.filename}")
        print(stdout.readline(), stderr.readline())


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'index/index.html'


class AddTempView(LoginRequiredMixin, TemplateView, View):
    login_url = '/login/'
    template_name = 'client/add.html'

    def get_context_data(self, **kwargs):
        form = forms.HostListForm()
        context = super(AddTempView, self).get_context_data(**kwargs)
        context['form'] = form
        return context


class GetClientListView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        search = request.POST
        pageSize = int(search.get('limit'))
        pageNumber = (int(search.get('offset')) / pageSize) + 1
        right_boundary = pageSize * pageNumber
        articles = HostList.objects.all()[(pageNumber - 1) * pageSize:right_boundary]
        total = HostList.objects.all().count()
        rows = []
        for article in articles:
            rows.append(
                {'id': article.id, 'domain': article.domain, 'host_user': article.host_user, 'host_ip': article.host_ip,
                 'host_name': article.host_name, 'host_port': article.host_port,
                 'Status': server_status(article.host_ip)})
        return JsonResponse({'code': 200, 'rows': rows, 'total': total})


class ClientListView(TemplateView, GetClientListView):
    template_name = 'client/list.html'


class DeployListView(TemplateView, GetClientListView):
    template_name = 'client/deploy.html'


class hostlist(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        list = HostList.objects.all()
        result_serialize = serializers.serialize('json', list)
        return HttpResponse(result_serialize, "application/json")


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
            print(form.errors.as_json())
            return HttpResponse(form.errors.as_json())


class DelHostList(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        data = request.POST
        try:
            list = HostList.objects.filter(id=data['id'])
            list.delete()
            return HttpResponse('{"status": "true", "msg": "删除成功"}', content_type="application/json")
        except Exception as e:
            return HttpResponse('{"status": "false", "msg": "%s"}' % e, content_type="application/json")


class EditHostList(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'client/edit.html'
    form_class = forms.HostListForm

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
        list = HostList.objects.get(id=request.POST.get('id'))
        file = request.FILES.getlist('web_file')
        plat = request.POST.get('option')

        if not os.path.exists(localpath):
            os.mkdir(localpath)
        if plat == '1':
            for f in file:
                with open(localpath + f.name, 'wb+') as fs:
                    for chunk in f.chunks():
                        fs.write(chunk)
                        # fs.close()
                SshUpload(list.host_ip, list.host_port, list.host_user, list.host_password, f.name, localpath,
                          list.des_path, list.dep_path).run()
        elif plat == '2':
            pass

        return HttpResponse('{"status": "true", "msg": "成功"}', content_type="application/json")


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
