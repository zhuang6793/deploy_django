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
    form_class = forms.HostListForm
    success_url = '/#hostlist/'

    def get(self, reuqest, **kwargs):
        self.object = HostList.objects.get(id = self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = HostList.objects.get(id = self.kwargs['id'])
        return obj




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


def Deploy(request):
    return render(request, 'Deploy.html')


def Install(request):
    return render(request, 'Install.html')


def Monitor(request):
    return render(request, 'Monitor.html')


def Site(request):
    return render(request, 'Site.html')
