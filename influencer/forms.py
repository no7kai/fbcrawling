from django import forms


class SearchIdForm(forms.Form):
    uid = forms.CharField(label="Enter user Id", max_length=100)


class SearchNameForm(forms.Form):
    name = forms.CharField(label="Enter user name", max_length=100)


class SearchPost(forms.Form):
    from_date = forms.DateField(
        label="From",
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    to_date = forms.DateField(
        label="To",
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))


class UpdateUserForm(forms.Form):
    uid = forms.CharField(label='Enter user Id again', max_length=100)
    from_date = forms.DateField(
        label="From",
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    to_date = forms.DateField(
        label="To",
        widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
