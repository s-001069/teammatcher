from django import forms
from .models import TeamNameTemplate


class UploadFileForm(forms.Form):
    """
        Form for uploading CSV and setting team formation criteria
    """
    file = forms.FileField(
        label='Select CSV File',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )
    min_team_size = forms.IntegerField(
        min_value=1,
        initial=3,
        label="Min People Per Team",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )
    max_team_size = forms.IntegerField(
        min_value=1,
        initial=5,
        label="Max People Per Team",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
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
    weight_availability = forms.IntegerField(
        label='Availability Weight',
        min_value=0,
        max_value=10,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    weight_commitment = forms.IntegerField(
        label='Commitment Weight',
        min_value=0,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    weight_education = forms.IntegerField(
        label='Educational Background Weight',
        min_value=0,
        max_value=10,
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    weight_job = forms.IntegerField(
        label='Professional Background Weight',
        min_value=0,
        max_value=10,
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    weight_age = forms.IntegerField(
        label='Age Weight',
        min_value=0,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    weight_gender = forms.IntegerField(
        label='Gender Weight',
        min_value=0,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    weight_experience = forms.IntegerField(
        label='Experience Weight',
        min_value=0,
        max_value=10,
        initial=6,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    weight_lead = forms.IntegerField(
        label='Lead Preference Weight',
        min_value=0,
        max_value=10,
        initial=6,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
    weight_tasks = forms.IntegerField(
        label='Preferred Tasks Weight',
        min_value=0,
        max_value=10,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1'
        })
    )
