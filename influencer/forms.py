from django import forms


class SearchIdForm(forms.Form):
    uid = forms.CharField(label="Enter user Id", max_length=100)


class SearchNameForm(forms.Form):
    name = forms.CharField(label="Enter user name", max_length=100)
