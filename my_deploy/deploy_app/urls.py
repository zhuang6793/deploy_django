from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from . import views

app_name = 'deploy_app'

urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'dashboard/', views.Dashboard, name='dashboard'),
    path(r'deploy/', views.Deploy, name='deploy'),
    path(r'hostlist/', views.AddHostList.as_view(), name='hostList'),
    re_path(r'^hostlist/update/(?P<pk>[0-9]+)/$', views.HostListUpdateView.as_view(), name='hostListUpdate'),
    # re_path(r'^hostlist/delete/(?P<pk>[0-9]+)/$', views.DeleteHostListView.as_view(), name='hostListDelete'),
    path(r'hostlist/delete', views.DeleteView.as_view(), name='hostListDelete'),
    path(r'hostlist/test_connect', views.HostTestConnectView.as_view(), name='hostTestConnect'),
    path(r'install/', views.InstallView.as_view(), name='install'),
    re_path(r'^test1/(?P<y>\d{4})/(?P<m>\d{1,2})/(?P<d>\d{1,2})$', views.test1, name='test1'),
    re_path(r'^test1/(?P<m>\d{1,2})/(?P<d>\d{1,2})/(?P<y>\d{4})$', views.test1, name='test1'),
    path(r'monitor/', views.Monitor, name='monitor'),
    path(r'site/', views.Site, name='site'),
    path(r'bootstrap/', views.Bootstrap, name='site'),
    path(r'index/', views.IndexView.as_view(), name='index'),
    path(r'client/list', views.GetClientListView.as_view(), name='list'),
    path(r'client/add', views.AddHostList.as_view(), name='add')
]

urlpatterns += staticfiles_urlpatterns()
