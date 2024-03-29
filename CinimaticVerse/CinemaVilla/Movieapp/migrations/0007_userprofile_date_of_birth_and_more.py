# Generated by Django 4.2.9 on 2024-02-04 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Movieapp', '0006_quality_remove_category_rating_movie_quality'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
