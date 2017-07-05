from django import forms

class DatabaseForm(forms.Form):
    db_name = forms.CharField()
    db_type = forms.IntegerField()
    host_ip = forms.CharField()
    db_manager_id = forms.IntegerField()
    detail = forms.CharField()