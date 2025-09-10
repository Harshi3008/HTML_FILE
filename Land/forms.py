from django import forms
from django.contrib.auth.models import User

class PenaltyFilterForm(forms.Form):
    month = forms.IntegerField(required=False, min_value=1, max_value=12, label="Month")
    year = forms.IntegerField(required=False, min_value=2000, max_value=2100, label="Year")
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="User",
        empty_label="All Users"
    )
