# Generated by Django 4.2.4 on 2023-08-31 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0003_friendrequest_insertiondate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='insertionDate',
            field=models.DateTimeField(),
        ),
    ]