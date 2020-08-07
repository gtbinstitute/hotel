# Generated by Django 2.0.2 on 2020-07-24 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomoptions', models.CharField(max_length=200)),
                ('roomprice', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='roomcategory',
            name='roomsavailable',
            field=models.TextField(default=0),
        ),
        migrations.AddField(
            model_name='roomdetails',
            name='roomcategoryid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.RoomCategory'),
        ),
    ]
