from django import forms
from .models import TeamNameTemplate


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select CSV File',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )
    team_size = forms.IntegerField(
        label='People per Team',
        min_value=1,
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter team size'
        })
    )
    team_template = forms.ModelChoiceField(
        queryset=TeamNameTemplate.objects.all(),
        required=False,
        empty_label="Default (Team 1, Team 2, ...)",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Team Name Template'
    )
