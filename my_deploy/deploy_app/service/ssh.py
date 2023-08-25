from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, ListView
from ..views import HostList
from django.shortcuts import render
from django.http import JsonResponse


# class GetClientListView(LoginRequiredMixin, View):
#     login_url = '/login/'
#
#     def post(self, request, *args, **kwargs):
#         search = request.POST
#         pageSize = int(search.get('limit'))
#         pageNumber = (int(search.get('offset')) / pageSize) + 1
#         right_boundary = pageSize * pageNumber
#         articles = HostList.objects.all()[(pageNumber - 1) * pageSize:right_boundary]
#         total = HostList.objects.all().count()
#         rows = []
#         for article in articles:
#             rows.append(
#                 {'id': article.id, 'domain': article.domain, 'host_user': article.host_user, 'host_ip': article.host_ip,
#                  'host_name': article.host_name, 'host_port': article.host_port,
#                  'Status': server_status(article.host_ip)})
#         return JsonResponse({'code': 200, 'rows': rows, 'total': total})


class SshView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        hostlist = HostList.objects.all()
        return render(request, 'client/ssh.html', {"hostlist": hostlist})
