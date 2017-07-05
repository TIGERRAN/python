from __future__ import unicode_literals

from django.db import models

# Create your models here.
class sys(models.Model):
    sys_id = models.AutoField(primary_key=True)
    sys_name = models.CharField(max_length=64)
    owner_id  = models.IntegerField()
    pd_id 	= models.IntegerField()
    c_t 	= models.DateTimeField()

    def __unicode__(self):
        ret = {'sys_id': self.sys_id, 'sys_name': self.sys_name, 'owner_id': self.owner_id,
               'pd_id': self.pd_id, 'c_t': self.c_t}
        return ret

class project(models.Model):
    pjt_id = models.AutoField(primary_key=True)
    sys_id =models.IntegerField()
    project_name =models.CharField(max_length=64)
    git_addr= models.CharField(max_length=128)
    db_id = models.IntegerField()
    c_t = models.DateTimeField()

    def __unicode__(self):
        ret = {'pjt_id': self.pjt_id, 'sys_id': self.sys_id, 'project_name': self.project_name,
               'git_addr': self.git_addr,'db_id':self.db_id, 'c_t': self.c_t}
        return ret