# Generated by Django 3.0.5 on 2020-06-07 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digifarming', '0005_auto_20200607_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order_item_cost',
            field=models.IntegerField(default=0),
        ),
    ]
