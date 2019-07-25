from django.db import models
from django.conf import settings

# Create your models here.


class Blog(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	comment = models.TextField()
	commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.blog}  {self.commented_by}'
