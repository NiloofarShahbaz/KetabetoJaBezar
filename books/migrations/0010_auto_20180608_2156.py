# Generated by Django 2.0.3 on 2018-06-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_book_isbn'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=300)),
                ('pic', models.URLField()),
                ('ISBN', models.CharField(max_length=17)),
                ('translator', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='translator',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
