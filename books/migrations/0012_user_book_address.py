# Generated by Django 2.0.3 on 2018-06-13 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_auto_20180613_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_book',
            name='address',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='books.Location'),
            preserve_default=False,
        ),
    ]
