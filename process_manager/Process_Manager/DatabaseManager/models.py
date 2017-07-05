from __future__ import unicode_literals

from django.db import models

# Create your models here.
class hosts(models.Model):
    host_id = models.AutoField(primary_key=True)
    sys_id = models.IntegerField()
    host_ip	= models.CharField(max_length=32)
    ssh_port = models.IntegerField()
    app_dir = models.CharField(max_length=64)
    service_port = models.IntegerField()
    env_id 	= models.IntegerField()
    c_t	= models.DateTimeField()

class env(models.Model):
    env_id = models.AutoField(primary_key=True)
    env_name = models.CharField(max_length=64)
    c_t	= models.DateTimeField()

class db_info(models.Model):
    db_id = models.AutoField(primary_key=True)
    db_name = models.CharField(max_length=32)
    env_id = models.IntegerField()
    host_ip = models.CharField(max_length=32)
    port = models.CharField(max_length=32)
    host_name = models.CharField(max_length=128)
    slave_db_id = models.IntegerField()
    db_type = models.IntegerField()
    c_t	= models.DateTimeField()
    manager_id = models.IntegerField()
    detail = models.CharField(max_length=256,null=True)

    def __unicode__(self):
        ret = {'db_id':self.db_id, 'db_name':self.db_name, 'env_id':self.env_id,'host_ip':self.host_ip,'port':self.port,'manager_id':self.manager_id,'c_t':self.c_t, 'detail':self.detail}
        return ret