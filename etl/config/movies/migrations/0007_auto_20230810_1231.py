# Generated by Django 3.2 on 2023-08-10 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_genre_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={
                'verbose_name': 'Персона',
                'verbose_name_plural': 'Персоны',
            },
        ),
        migrations.AddField(
            model_name='personfilmwork',
            name='role',
            field=models.TextField(blank=True, null=True, verbose_name='role'),
        ),
    ]