# Generated by Django 2.0.3 on 2018-06-14 13:35

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0016_auto_20180614_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='picture',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='user_book',
            name='release_date',
            field=django_jalali.db.models.jDateTimeField(),
        ),
    ]