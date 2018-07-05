# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecvInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recv_username', models.CharField(max_length=20)),
                ('recv_addr', models.CharField(max_length=100)),
                ('recv_phone', models.CharField(max_length=11)),
                ('recv_postcode', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=30)),
                ('uphone', models.CharField(max_length=11)),
                ('uaddress', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='recvinfo',
            name='uid',
            field=models.ForeignKey(to='df_user.UserInfo'),
        ),
    ]
