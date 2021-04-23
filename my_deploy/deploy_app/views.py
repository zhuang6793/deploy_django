from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from deploy_app.models import HostList
import os

def index(request):
    list = [{id: 1, 'name': 'huangz', 'age': 29}, {id: 2, 'name': 'cly', 'age': 29}]
    return render(request, 'index.html', {'students': list})


def shouye(request):
    return render(request, 'shouye.html')


@csrf_exempt
def Host_List(request):
    if request.method == "POST":
        host_name = request.POST.get("host_name", None)
        ip = request.POST.get("ip_add", None)
        domain = request.POST.get("domain", None)
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        port = request.POST.get("port", None)
        key_file = request.FILES.get("key_file")
        key_path = None
        if key_file != None:
            if os.path.exists('./key_file'):
                key_path = './key_file/' + key_file.name
                with open('./key_file/'+key_file.name, 'wb') as f:
                    for chunk in key_file:
                        f.write(chunk)
            else:
                os.mkdir('./key_file')
        hostlist = HostList(host_name=host_name, host_ip=ip, domain=domain, host_user=username, host_password=password, host_port=port, host_key_file=key_path)
        hostlist.save()

    hostlist = HostList.objects.all()

    return render(request, 'HostList.html', {'hostlist':hostlist})

@csrf_exempt
def Edit_Host_List(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        hostlist = HostList.objects.filter(id=id)

    return render(request, "HostList.html", {'edit_list': hostlist[0]})



def Deploy(request):
    return render(request, 'Deploy.html')

def Install(request):
    return render(request, 'Install.html')

def Monitor(request):
    return render(request, 'Monitor.html')

def Site(request):
    return render(request, 'Site.html')
