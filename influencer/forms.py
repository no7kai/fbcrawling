from django import forms


class FilterForm(forms.Form):
    text = forms.CharField(max_length=250, required=False)
    created_lte = forms.DateField(required=False)
    created_gte = forms.DateField(required=False)
    likes_lte = forms.IntegerField(required=False)
    likes_gte = forms.IntegerField(required=False)
