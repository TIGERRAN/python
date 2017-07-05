from __future__ import unicode_literals
from django.db import models

# Create your models here.
class group(models.Model):
    grp_id = models.AutoField(primary_key=True)
    grp_name = models.CharField(max_length=64)
    c_t = models.DateTimeField()
    detail = models.CharField(max_length=256,null=True)

    def __unicode__(self):
        ret = {'grp_id':self.grp_id, 'name':self.grp_name, 'c_t':self.c_t, 'detail':self.detail}
        return ret