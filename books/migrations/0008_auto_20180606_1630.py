# Generated by Django 2.0.3 on 2018-06-06 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_book_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='picture',
            field=models.URLField(),
        ),
    ]