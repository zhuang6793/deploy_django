from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from . import views
from .service import add, client, deploy, ssh

app_name = 'deploy_app'

urlpatterns = [
    re_path(r'^hostlist/update/(?P<pk>[0-9]+)/$', views.HostListUpdateView.as_view(), name='hostListUpdate'),
    path(r'hostlist/delete', views.DeleteView.as_view(), name='hostListDelete'),
    path(r'hostlist/test_connect', views.HostTestConnectView.as_view(), name='hostTestConnect'),
    path(r'install/', views.InstallView.as_view(), name='install'),
    path(r'monitor/', views.Monitor, name='monitor'),
    path(r'site/', views.Site, name='site'),
    path(r'bootstrap/', views.Bootstrap, name='site'),
    path(r'index/', views.IndexView.as_view(), name='index'),
    path(r'client/list', client.ClientListView.as_view(), name='list'),
    path(r'client/add', add.AddHostList.as_view(), name='add'),
    path(r'client/del/', views.DelHostList.as_view(), name='del'),
    path(r'client/edit', views.EditHostList.as_view(), name='edit'),
    path(r'client/deploy', deploy.DeployListView.as_view(), name='deploy'),
    path(r'client/exec', deploy.ExecHost.as_view(), name='exec'),
    path(r'client/ssh', ssh.SshView.as_view(), name='ssh')
]

urlpatterns += staticfiles_urlpatterns()
