from django import forms
import datetime


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

    # def clean_uid(self, *args, **kwargs):
    #     uid = self.cleaned_data.get('uid')
    #     qs = User.objects.filter(uid=uid)
    #     if qs.exists():
    #         raise forms.ValidationError("This user is already in database. Please search again.")
    #     return uid

    def clean_from_date(self, *args, **kwargs):
        from_date = self.cleaned_data.get('from_date')
        if from_date.year == 2018:
            raise forms.ValidationError("Invalidate year.")
        if from_date < datetime.date.today() - datetime.timedelta(days=4):
            raise forms.ValidationError("Invalidate day.")
        return from_date
