# Generated by Django 2.0.3 on 2018-04-30 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default='hello!this is my bio!', max_length=500),
        ),
    ]