from __future__ import unicode_literals

from django.db import models

# Create your models here.
class workorder(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=64)
    applicant_id = models.IntegerField()
    order_type = models.IntegerField()
    bug_id = models.IntegerField(null=True)
    sys_id = models.IntegerField()
    pj_id = models.IntegerField()
    db_id =  models.IntegerField(null=True)
    branch = models.CharField(max_length=64)
    auto_deploy = models.IntegerField()
    db_change = models.IntegerField(null=True)
    cf_change = models.IntegerField(null=True)
    detail = models.CharField(max_length=4096)
    rely_project = models.CharField(max_length=128,null=True)
    online_detail = models.CharField(max_length=4096,null=True)
    conf_detail = models.CharField(max_length=4096,null=True)
    effect_detail = models.CharField(max_length=4096,null=True)
    status = models.IntegerField()
    c_t = models.DateTimeField(null=True)
    u_t = models.DateTimeField(null=True)

    def __unicode__(self):
        ret = {'order_id':self.id,'order_name':self.order_name, 'order_typr':self.order_type,'sys_id':self.sys_id, 'pj_id':self.pj_id,'db_id':self.db_id,'auto_deploy':self.auto_deploy,'applicant_id':self.applicant_id,'status':self.status,'c_t':self.c_t,'u_t':self.u_t}
        return ret

class workorder_project(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=64)
    applicant_id = models.IntegerField()
    order_type = models.IntegerField()
    db_change = models.IntegerField(null=True)
    pj_ids = models.CharField(max_length=128)
    stage_time = models.DateTimeField()
    online_time = models.DateTimeField()
    status = models.IntegerField()
    c_t = models.DateTimeField(null=True)
    u_t = models.DateTimeField(null=True)

    def __unicode__(self):
        ret = {'id':self.id,'order_name':self.order_name, 'order_typr':self.order_type,'db_change':self.db_change,'pj_ids':self.pj_ids,'applicant_id':self.applicant_id,'stage_time':self.stage_time,'online_time':self.online_time,'status':self.status,'c_t':self.c_t,'u_t':self.u_t}
        return ret

class workorder_sql(models.Model):
    id = models.AutoField(primary_key=True)
    workorder_id = models.IntegerField()
    type = models.IntegerField()
    pjt_id = models.IntegerField()
    db_id = models.IntegerField()
    sql_value = models.CharField(max_length=128)
    c_t = models.DateTimeField()

class workorder_status(models.Model):
    id = models.AutoField(primary_key=True)
    workorder_id = models.IntegerField()
    type = models.IntegerField()
    pjt_id = models.CharField(max_length=128)
    auditor = models.IntegerField(null=True)
    status = models.IntegerField()
    c_t = models.DateTimeField(null=True)

class workorder_auto_deploy(models.Model):
    id = models.AutoField(primary_key=True)
    workorder_id = models.IntegerField()
    result = models.IntegerField(null=True)
    log = models.CharField(max_length=4096,null=True)
    c_t = models.DateTimeField(null=True)