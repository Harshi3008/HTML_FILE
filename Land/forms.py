from django import forms
from .models import Membership

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = [
            'full_name',
            'age',
            'mobile_number',
            'email',
            'address',
            'profession',
            'plan_choice',
            'aadhar_card_number',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'plan_choice': forms.Select(attrs={'class': 'form-control'}),
            'aadhar_card_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
