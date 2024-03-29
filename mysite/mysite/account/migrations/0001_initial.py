# Generated by Django 2.1.5 on 2019-02-24 10:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, error_messages={'unique': 'A user with the username already exists'}, help_text='Required 150 or fewer charecters. Letters digits and @/..only', max_length=150, verbose_name='username')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether this user an log into admin site', verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates whether this user can log into admin site', verbose_name='Superuser status')),
                ('is_active', models.BooleanField(default=True, help_text='designates whether this user should be treated as activeUnselect this instead of deleating accounts.', verbose_name='active')),
                ('is_author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
