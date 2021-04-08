from django.shortcuts import render

def index(request):
    list = [{id: 1, 'name': 'huangz', 'age': 29}, {id: 2, 'name': 'cly', 'age': 29}]
    return render(request, 'index.html', {'students': list})
