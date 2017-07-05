from __future__ import unicode_literals
from django.db import models

# Create your models here.
class user(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    grp_id = models.IntegerField()
    c_t = models.DateTimeField()

    def __unicode__(self):
        ret = {'id':self.id,'user':self.user,'username':self.username,'email':self.email,'grp_id':self.grp_id,'c_t':self.c_t}
        return ret