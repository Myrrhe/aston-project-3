# Generated by Django 4.2.4 on 2023-12-18 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_topicsection_remove_topic_post_topic_content_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at', '-updated_at'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['-created_at', '-updated_at'], 'verbose_name': 'Topic', 'verbose_name_plural': 'Topics'},
        ),
        migrations.AlterModelOptions(
            name='topicsection',
            options={'ordering': ['-created_at', '-updated_at'], 'verbose_name': 'Section de topic', 'verbose_name_plural': 'Sections de topic'},
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, help_text='Le contenu du post', max_length=4096, null=True, verbose_name='Contenu'),
        ),
        migrations.AlterField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Le post a-t-il été supprimé', verbose_name='Supprimé'),
        ),
        migrations.AlterField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(help_text='Le topic du post', on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='forum.topic', verbose_name='Topic'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(help_text="L'auteur du poste", null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=models.TextField(blank=True, help_text='Le contenu du post', max_length=4096, null=True, verbose_name='Contenu'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Le post a-t-il été supprimé', verbose_name='Supprimé'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='section',
            field=models.ForeignKey(help_text='La section du topic', null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.topicsection', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(blank=True, help_text='Le titre du topic', max_length=50, null=True, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(help_text="L'auteur du topic'", null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0, help_text='Le nombre de vues du topic', verbose_name='Vues'),
        ),
        migrations.AlterField(
            model_name='topicsection',
            name='code',
            field=models.CharField(default=False, help_text='Le code de la section', max_length=64, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='topicsection',
            name='description',
            field=models.TextField(default=False, help_text='La description de la section', max_length=4096, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='topicsection',
            name='name',
            field=models.CharField(default=False, help_text='Le nom de la section', max_length=64, verbose_name='Nom'),
        ),
    ]