# Generated by Django 4.0.3 on 2022-06-19 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='static/images'),
        ),
    ]
