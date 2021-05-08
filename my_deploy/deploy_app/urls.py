from django.urls import path,re_path

from . import views

app_name = 'deploy_app'

urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
    path(r'dashboard/', views.Dashboard, name='dashboard'),
    path(r'deploy/', views.Deploy, name='deploy'),
    path(r'hostlist/', views.AddHostList.as_view(), name='hostlist'),
    path(r'update/', views.HostListUpdateView.as_view(), name='hostlistupdate'),
    path(r'install/', views.Install, name='install'),
    path(r'monitor/', views.Monitor, name='monitor'),
    path(r'site/', views.Site, name='site')
]
