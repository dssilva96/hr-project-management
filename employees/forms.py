from django import forms

from .models import Employee, Team


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user',
            'first_name',
            'last_name',
            'email',
            'position',
            'mobile',
            'department',
            'status',
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'lead', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'lead': forms.Select(attrs={'class': 'form-select'}),
            'members': forms.CheckboxSelectMultiple(attrs={'class': 'team-member-options'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        lead = cleaned_data.get('lead')
        members = cleaned_data.get('members')

        if lead and members and lead not in members:
            cleaned_data['members'] = list(members) + [lead]

        return cleaned_data
