from django import forms
from blog.models import Blog, Comment



class BlogForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ['title' ,'description', 'image']


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment']

from django.contrib.auth.models import User

class UserSignupForm(forms.ModelForm):

	password1 = forms.CharField(label='Passsword', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Passsword conformation', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ('username','email')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("passwords don't match")
			return password2

	def save(self, commit=True):
		user = super(UserSignupForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user