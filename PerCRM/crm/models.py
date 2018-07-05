# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


# Create your models here.
class Customer(models.Model):
    '''
    客户表
    '''
    name = models.CharField(max_length=32, blank=True, null=True)
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    source_choices = (
        (0, u'转介绍'),
        (1, u'QQ群'),
        (2, u'官网'),
        (3, u'百度推广'),
        (4, u'51CTO'),
        (5, u'市场推广'),
    )
    source = models.PositiveSmallIntegerField(choices=source_choices)
    referral_from = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'转介绍人QQ')
    consult_course = models.ForeignKey('Course', verbose_name=u'咨询课程')
    content = models.TextField(verbose_name=u'咨询课程详情')
    consultant = models.ForeignKey('UserProfile', verbose_name=u'咨询人')
    status_choices = (
        (0, '已报名'),
        (1, '未报名'),
    )
    status = models.SmallIntegerField(choices=status_choices, default=0)
    note = models.TextField(blank=True, null=True)
    flags = models.ManyToManyField('Tags', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name = u'客户表'
        verbose_name_plural = u'客户表'


class Tags(models.Model):
    '''
    标签信息
    '''
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'标签表'
        verbose_name_plural = u'标签表'


class CustomerFollowUp(models.Model):
    '''
    客户跟进记录
    '''
    customer = models.ForeignKey('Customer')
    content = models.TextField(verbose_name='跟进内容')
    consultant = models.ForeignKey('UserProfile', verbose_name='跟进人')
    date = models.DateTimeField(auto_now_add=True)
    intention_choices = (
        (0, u'2周内报名'),
        (1, u'一个月内报名'),
        (2, u'近期无报名计划'),
        (3, u'已在其他机构报名'),
        (4, u'已报名'),
        (0, u'已拉黑'),
    )
    intention = models.PositiveSmallIntegerField(choices=intention_choices, verbose_name=u'状态')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<{}:{}>'.format(self.customer.qq, self.intention)

    class Meta:
        verbose_name = u'客户跟进表'
        verbose_name_plural = u'客户跟进表'


class Course(models.Model):
    '''
    课程表
    '''
    name = models.CharField(max_length=64, unique=True)
    price = models.PositiveIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name=u'周期(月)')
    outline = models.TextField(verbose_name=u'大纲')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'课程表'
        verbose_name_plural = u'课程表'


class ClassList(models.Model):
    '''
    班级表
    '''
    course = models.ForeignKey('Course', verbose_name=u'班级课程')
    branch = models.ForeignKey('Branch', verbose_name=u'校区')
    semester = models.PositiveSmallIntegerField(verbose_name=u'学期')
    teachers = models.ManyToManyField('UserProfile')
    class_type_choices = (
        (0, u'面授(脱产)'),
        (1, u'面授(周末)'),
        (2, u'网络'),
    )
    class_type = models.PositiveSmallIntegerField(choices=class_type_choices, verbose_name=u'班级类型')
    start_date = models.DateField(verbose_name=u'开班日期')
    end_date = models.DateField(verbose_name=u'毕业日期', blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.branch, self.course, self.semester)

    class Meta:
        unique_together = ('branch', 'course', 'semester',)
        verbose_name = u'班级表'
        verbose_name_plural = u'班级表'



class Branch(models.Model):
    '''
    校区
    '''
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'校区表'
        verbose_name_plural = u'校区表'


class CourseRecord(models.Model):
    '''
    上课记录
    '''
    from_class = models.ForeignKey('ClassList', verbose_name=u'班级')
    day_num = models.PositiveSmallIntegerField(verbose_name=u'第几节(天)')
    teacher = models.ForeignKey('UserProfile')
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=32, blank=True, null=True)
    outline = models.TextField(verbose_name=u'本节课大纲')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.from_class, self.day_num)

    class Meta:
        unique_together = ('from_class', 'day_num',)
        verbose_name = u'上课记录'
        verbose_name_plural = u'上课记录'


class StudyRecord(models.Model):
    '''
    学习记录
    '''
    student = models.ForeignKey('Enrollment')
    course_record = models.ForeignKey('CourseRecord')
    attendance_choices = (
        (0, u'已签到'),
        (1, u'迟到'),
        (2, u'缺勤'),
        (3, u'早退'),
    )
    attendance = models.PositiveSmallIntegerField(choices=attendance_choices, default=0)
    score_choices = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (75, 'B-'),
        (70, 'C+'),
        (60, 'C'),
        (40, 'C-'),
        (-50, 'D'),
        (-100, 'copy'),
        (0, 'N/A'),
    )
    score = models.SmallIntegerField(choices=score_choices)
    note = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{} {} {}'.format(self.student, self.course_record, self.score)

    class Meta:
        unique_together = ('student', 'course_record', 'score',)
        verbose_name = u'学习记录表'
        verbose_name_plural = u'学习记录表'


class Enrollment(models.Model):
    '''
    报名表
    '''
    customer = models.ForeignKey('Customer')
    enrolled_class = models.ForeignKey('ClassList', verbose_name=u'所报班级')
    consultant = models.ForeignKey('UserProfile', verbose_name=u'课程顾问')
    contract_agreed = models.BooleanField(default=False, verbose_name=u'学员已同意合同条款')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.customer, self.enrolled_class)

    class Meta:
        unique_together = ('customer', 'enrolled_class')
        verbose_name = u'报名表'
        verbose_name_plural = u'报名表'


class Payment(models.Model):
    '''
    缴费表
    '''
    customer = models.ForeignKey('Customer')
    course = models.ForeignKey('Course', verbose_name=u'所报课程')
    amount = models.PositiveIntegerField(verbose_name=u'数额', default=500)
    consultant = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.customer, self.amount)

    class Meta:
        verbose_name = u'缴费表'
        verbose_name_plural = u'缴费表'


class Role(models.Model):
    '''
    角色表
    '''
    name = models.CharField(max_length=32, unique=True)
    menu = models.ManyToManyField('Menu', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'角色表'
        verbose_name_plural = u'角色表'


class UserProfile(AbstractUser):
    '''
    账户表，扩展django自带的User表
    '''
    # name = models.CharField(max_length=32, verbose_name=u'用户名')
    roles = models.ManyToManyField('Role', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = u'账户表'
        verbose_name_plural = u'账户表'


class Menu(models.Model):
    '''
    菜单表
    '''
    name = models.CharField(max_length=32)
    url_name = models.CharField(max_length=64, default='/crm/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'菜单表'
        verbose_name_plural = u'菜单表'