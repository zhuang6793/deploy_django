from django.db import models

# Create your models here.

class HostList(models.Model):
    host_name = models.CharField(max_length=200)
    host_ip = models.CharField(max_length=200)
    host_user = models.CharField(max_length=200)
    host_password = models.CharField(max_length=200, default='', null=True, blank=True)
    host_port = models.IntegerField(default=22)
    host_key_file = models.FileField(upload_to='key_file', null=True, blank=True)
    domain = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.host_name

