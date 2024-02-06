# Generated by Django 4.2.9 on 2024-01-30 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movieapp', '0005_movie_movie_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='category',
            name='rating',
        ),
        migrations.AddField(
            model_name='movie',
            name='quality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Movieapp.quality'),
        ),
    ]