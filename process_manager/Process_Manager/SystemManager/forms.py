# -*- coding: utf-8 -*-
from django import forms

class Addsys(forms.Form):
    sys_name = forms.CharField(max_length=64)
    owner_id = forms.IntegerField()
    pd_id = forms.IntegerField()


class set_sys(forms.Form):
    sys_id = forms.IntegerField()
    sys_name = forms.CharField(max_length=64)
    owner_id = forms.IntegerField()
    pd_id = forms.IntegerField()

class Add_pj_form(forms.Form):
	sys_id = forms.IntegerField()
	project_name = forms.CharField(max_length=64)
	git_addr= forms.CharField(max_length=256)
	db_id = forms.IntegerField()

class Up_pj_form(forms.Form):
	pjt_id 		= forms.IntegerField()
	sys_id 		= forms.IntegerField()
	project_name= forms.CharField(max_length=64)
	git_addr	= forms.CharField(max_length=256)
	db_id 		= forms.IntegerField()