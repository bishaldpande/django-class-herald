from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['first_name', 'middle_name', 'last_name', 
				'contact', 'email', 'gender', 'image']
