# Generated by Django 4.2.2 on 2023-07-05 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_alter_film_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='poster',
            field=models.ImageField(default='C:/Users/Peter/Desktop/film_rate/media/1.jpg', upload_to='posters/'),
        ),
    ]