# Generated by Django 3.0.5 on 2020-04-27 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digifarming', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_client',
            field=models.ForeignKey(default=100, on_delete=django.db.models.deletion.CASCADE, to='digifarming.Client'),
            preserve_default=False,
        ),
    ]
