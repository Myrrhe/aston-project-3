# Generated by Django 4.2.4 on 2023-11-03 08:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(help_text="L'email de l'utilisateur", max_length=50, unique=True, verbose_name='Email')),
                ('username', models.CharField(help_text="Le nom utilisé par l'utilisateur", max_length=50, null=True, verbose_name="Nom d'utilisateur")),
                ('language', models.CharField(choices=[('EN', 'English'), ('FR', 'Français'), ('ES', 'Español')], default='FR', max_length=2)),
                ('theme', models.CharField(choices=[('DARK', 0), ('LIGHT', 1), ('AUTO', 2)], default='AUTO')),
                ('is_email_confirmed', models.BooleanField(default=False, help_text="L'adresse email a-t-elle été vérifiée", verbose_name='Email confirmé')),
                ('is_tou_accepted', models.BooleanField(default=False, help_text="Les conditions d'utilisations ont-elles été acceptées par l'utilisateur", verbose_name="Conditions d'utilisations")),
                ('is_admin', models.BooleanField(default=False, help_text="L'utilisateur est-il un administrateur", verbose_name='Admin')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utilisateur',
                'verbose_name_plural': 'Utilisateurs',
                'db_table': 'user',
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
