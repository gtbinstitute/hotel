# Generated by Django 2.0.2 on 2020-07-27 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0004_auto_20200725_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomcategory',
            name='Image',
            field=models.ImageField(blank='True', null='True', upload_to='pics'),
        ),
    ]
