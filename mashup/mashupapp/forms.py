from django import forms

from .models import mashup_data


class mashup_form(forms.ModelForm):
    class Meta:
        model = mashup_data
        fields = ('singername', 'n_videos', 'duration', 'email')
