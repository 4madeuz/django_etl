# Generated by Django 3.2 on 2023-08-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmwork', old_name='created', new_name='created_at',
        ),
        migrations.RenameField(
            model_name='filmwork', old_name='modified', new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='genre', old_name='created', new_name='created_at',
        ),
        migrations.RenameField(
            model_name='genre', old_name='modified', new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='genrefilmwork',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='person', old_name='created', new_name='created_at',
        ),
        migrations.RenameField(
            model_name='person', old_name='modified', new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='personfilmwork',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='filmwork',
            name='file_path',
            field=models.FilePathField(
                blank=True, null=True, path='movies/', verbose_name='file'
            ),
        ),
    ]
