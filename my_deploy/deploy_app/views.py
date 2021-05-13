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
    template_name = 'UpdateHostList.html'
    form_class = forms.HostListForm
    success_url = '/#hostlist/'

    def get(self, request, *args, **kwargs):
        adv_positin = HostList.objects.get(id = self.kwargs['pk'])
        form = self.form_class(instance= adv_positin)
        return render( request, 'UpdateHostList.html', {'form': form, 'id': self.kwargs['pk']})


class AddHostList(HostListView, View):

    def post(self, request, *args, **kwargs):
        cursor = connection.cursor()
        form = forms.HostListForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cursor.execute("SET @i=0;")
            cursor.execute("UPDATE `deploy_app_hostlist` SET `id`=(@i:=@i+1);")
            cursor.execute("ALTER TABLE `deploy_app_hostlist` AUTO_INCREMENT=0;")
            return redirect("/#hostlist")
        else:

            return HttpResponse(form.errors)



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

def test1(request):
    return render(request, 'bootstrap-test.html')
