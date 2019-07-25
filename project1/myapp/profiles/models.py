from django.db import models
from django.conf import settings

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, blank=True)
	last_name = models.CharField(max_length=100)

	contact = models.CharField(max_length=20, blank=True)
	email = models.CharField(max_length=255)

	profiel_picture = models.ImageField(upload_to='profile/picture/%y/%m/',null=True, blank=True)

	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
		('O', 'Others'),
		)

	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

	def __str__(self):
		return ('{0} {1}').format(first_name, last_name)