from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        return render(request, 'index/index.html', {"user": request.user})


def login(request):
    if request.session.get('username') is not None:
        return HttpResponseRedirect('/', {"user": request.user})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect('/', {"user": request.user})
        else:
            if request.method == "POST":
                return render(request, 'index/login.html', {"login_error_info": "用户名或者密码错误", "username": username}, )
            else:
                return render(request, 'index/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')
