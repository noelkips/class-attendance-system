# Generated by Django 4.1.1 on 2022-11-05 20:07

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('learningAttendance', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Registration/Payroll Number')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], help_text='only applicable to student', null=True)),
                ('semester', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3)], help_text='only applicable to student', null=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to=users.models.profile_pic_path, verbose_name='profile picture')),
                ('is_staff', models.BooleanField(default=False, help_text='only applicable to lecturer.', verbose_name='Lecturer')),
                ('course', models.ForeignKey(blank=True, help_text='only applicable to student', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='learningAttendance.course', verbose_name='Student Course')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('school', models.ForeignKey(blank=True, help_text='only applicable to student', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schools', to='learningAttendance.school', verbose_name='Student Faculty')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
