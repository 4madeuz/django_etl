# Generated by Django 3.2 on 2023-08-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_filmwork_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='description',
            field=models.TextField(
                blank=True, null=True, verbose_name='description'
            ),
        ),
    ]
