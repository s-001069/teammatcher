from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select CSV File')
    team_size = forms.IntegerField(label='People per Team', min_value=1, initial=3)
