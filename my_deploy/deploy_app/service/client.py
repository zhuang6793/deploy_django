from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from ..views import HostList
import subprocess
import platform
from django.http import JsonResponse


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
