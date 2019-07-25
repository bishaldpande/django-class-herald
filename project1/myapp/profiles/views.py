from django.shortcuts import render

from django.shortcuts import redirect
from .models import Profile
from .forms import ProfileForm

# Create your views here.


def profile(request):
	try:
		profile = Profile.objects.get(user=request.user)

	except:
		return redirect('add-profile')


def add_profile(request):

	if request.method == 'POST':
		form = ProfileForm

