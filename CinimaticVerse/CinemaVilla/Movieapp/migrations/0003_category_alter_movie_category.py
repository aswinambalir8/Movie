# Generated by Django 4.2.9 on 2024-01-29 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movieapp', '0002_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movieapp.category'),
        ),
    ]
