from django.db import models

# Create your models here.

class HostList(models.Model):
    host_name = models.CharField(max_length=200)
    host_ip = models.CharField(max_length=200)
    host_user = models.CharField(max_length=200)
    host_password = models.CharField(max_length=200, default='')
    host_port = models.IntegerField(default=22)
    host_key_file = models.CharField(max_length=200)
