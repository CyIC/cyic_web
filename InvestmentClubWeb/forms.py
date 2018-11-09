from django import forms
from .models import JournalEntry


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('url', 'location', 'company')


class DuesForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ('credit_ledger', 'credit_amount')
