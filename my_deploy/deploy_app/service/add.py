from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db import connection
from .. import forms

from django.contrib.auth.mixins import PermissionRequiredMixin


class AddTempView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView, View):
    login_url = '/login/'
    template_name = 'client/add.html'
    permission_required = 'polls.can_vote'

    # permission_required = ('polls.can_open', 'polls.can_edit')
    def get_context_data(self, **kwargs):
        form = forms.HostListForm()
        context = super(AddTempView, self).get_context_data(**kwargs)
        context['form'] = form
        return context


class AddHostList(AddTempView, PermissionRequiredMixin, View):
    permission_required = 'polls.can_vote'

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
