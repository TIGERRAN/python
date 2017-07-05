from __future__ import unicode_literals
from django.db import models

# Create your models here
class db_backup_info(models.Model):
    id = models.AutoField(primary_key=True)
    db_id = models.CharField(max_length=64)
    day_of_week = models.CharField(max_length=64)
    hour = models.CharField(max_length=64)
    minute = models.CharField(max_length=64)
    status = models.IntegerField()
    is_running = models.IntegerField()
    shell_dir = models.CharField(max_length=128)

    def __unicode__(self):
        ret = {'id':self.id,'db_id':self.db_id,'day_of_week':self.day_of_week,'hour':self.hour,'minute':self.minute,'status':self.status,'is_running':self.is_running,'shell_dir':self.shell_dir}
        return ret