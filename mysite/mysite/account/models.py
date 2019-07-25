from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone

# Create your models here.
class UserManager(BaseUserManager):
	def _create_user(self, username, email,password, **extra_fields):
		if not email:
			raise ValueError('User must enter a email')

		email = self.normalize_email(email)

		user = self.model(username=username, email=email, **extra_fields)
		#  User(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		return self._create_user(username, email, password, **extra_fields)
	
	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff')is not True:
			raise ValueError('Super user must have is_staff = True')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True')
		return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(
		_('username'),
		max_length=150, blank=True, 
		help_text=_('Required 150 or fewer charecters. Letters digits and @/..only'),
		error_messages={
			'unique': _("A user with the username already exists"),
		},
		)
	email = models.EmailField(_('email address'), unique=True, null=True)

	is_staff = models.BooleanField(
		_('staff status'),
		default = False,
		help_text=_('Designates whether this user an log into admin site'))
	
	is_superuser= models.BooleanField(
		_('Superuser status'),
		default = False,
		help_text=_('Designates whether this user can log into admin site'))

	is_active = models.BooleanField(
		_('active'), default = True,
		help_text=_('designates whether this user should be treated as active'
					'Unselect this instead of deleating accounts.')
		)
	is_author = models.BooleanField(default=False)

	date_joined = models.DateTimeField(_('date joined'), default = timezone.now)

	objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def get_full_name(self):
		full_name = '%s'%self.username
		return full_name.strip()

	def get_short_name(self):
		return self.email

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)