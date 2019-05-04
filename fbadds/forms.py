from django import forms


class FindForm(forms.Form):
    find = forms.CharField(max_length=250)
