from django.shortcuts import render

def index(request):
    list = [{id: 1, 'name': 'huangz', 'age': 29}, {id: 2, 'name': 'cly', 'age': 29}]
    return render(request, 'index.html', {'students': list})


def shouye(request):
    return render(request, 'shouye.html')

def HostList(request):
    return render(request, 'HostList.html')

def Deploy(request):
    return render(request, 'Deploy.html')

def Install(request):
    return render(request, 'Install.html')

def Monitor(request):
    return render(request, 'Monitor.html')

def Site(request):
    return render(request, 'Site.html')
