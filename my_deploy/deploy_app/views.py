from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView
from django.db import connection
from deploy_app.models import HostList
from . import forms


class IndexView(TemplateView):
    template_name = 'index.html'


class HostListView(ListView):
    model = HostList
    template_name = 'HostList.html'
    context_object_name = "hostlist"

    def get_context_data(self, *, object_list=None, **kwargs):
        form = forms.HostListForm()
        context = super().get_context_data(**kwargs)
        context['hostlist'] = self.object_list.filter(is_active=True)
        context['form'] = form
        return context


class AddHostList(HostListView, View):

    def post(self, request, *args, **kwargs):
        cursor = connection.cursor()
        form = forms.HostListForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cursor.execute("SET @i=0;")
            cursor.execute("UPDATE `deploy_app_hostlist` SET `id`=(@i:=@i+1);")
            cursor.execute("ALTER TABLE `deploy_app_hostlist` AUTO_INCREMENT=0;")
            return redirect("/hostlist")
        else:
            return HttpResponse(form.errors)


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


def Install(request):
    return render(request, 'Install.html')


def Monitor(request):
    return render(request, 'Monitor.html')


def Site(request):
    return render(request, 'Site.html')


def test1(request, y, m, d):
    print(request.COOKIES)
    print(request.session)
    print(request.body)
    print(request.scheme)
    print(request.path_info)
    print(request.get_full_path())
    print(request.META['REMOTE_ADDR'])

    return render(request, 'asd.html', {"y": y, "m": m, "d": d})
