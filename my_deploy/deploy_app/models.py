from django.db import models


# Create your models here.

class HostList(models.Model):
    host_name = models.CharField('主机名', max_length=200)
    host_ip = models.CharField('IP地址', max_length=200)
    host_user = models.CharField('用户名', max_length=200)
    host_password = models.CharField('密码', max_length=200, default='', null=True, blank=True)
    host_port = models.IntegerField('端口', default=22)
    host_key_file = models.FileField('密钥', upload_to='key_file', null=True, blank=True)
    domain = models.CharField('域名', max_length=200, null=True, blank=True)
    is_active = models.BooleanField('是否活跃', default=True)

    class Meta:
        verbose_name = '主机列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s,%s,%s,%s,%s'%(self.host_name, self.host_ip, self.host_user, self.host_password, self.host_port)



class InstallServer(models.Model):
    host_status = models.IntegerField('主机状态', default=0)
    install_server = models.CharField('安装服务', max_length=200)
    host_id = models.ForeignKey(HostList, on_delete=models.CASCADE)


class Test(models.Model):
    t1 = models.CharField(max_length=10)
    t2 = models.CharField(max_length=10)
    num = models.IntegerField(max_length=50, default=0)


    def __str__(self):
        return '%s,%s,%s'%(self.t1, self.t2, self.num)