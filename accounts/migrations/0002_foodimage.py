# Generated by Django 5.0.4 on 2024-05-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
                ('predicted_food', models.CharField(max_length=100)),
                ('calories_data', models.JSONField()),
                ('predicted_volume', models.CharField(max_length=100)),
            ],
        ),
    ]
