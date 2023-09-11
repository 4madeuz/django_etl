# Generated by Django 3.2 on 2023-08-24 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_filmwork_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='type',
            field=models.TextField(
                choices=[('movie', 'Movie'), ('tv_show', 'Tv Show')],
                default='movie',
                null=True,
                verbose_name='type',
            ),
        ),
    ]
