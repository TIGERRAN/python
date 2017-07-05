from django import forms

class AddGroupForm(forms.Form):
    name = forms.CharField()
    enable = forms.IntegerField()
    detail = forms.CharField()

class EditGroupForm(forms.Form):
    grp_name = forms.CharField()
    members = forms.CharField()
    detail = forms.CharField()