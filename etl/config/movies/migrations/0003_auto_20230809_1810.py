# Generated by Django 3.2 on 2023-08-09 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20230809_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmwork',
            old_name='modified_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='genre', old_name='modified_at', new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='person', old_name='modified_at', new_name='updated_at',
        ),
    ]
