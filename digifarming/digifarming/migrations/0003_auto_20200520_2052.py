# Generated by Django 3.0.5 on 2020-05-20 20:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('digifarming', '0002_order_order_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancellationView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'CancellationView',
                'managed': False,
            },
        ),
        migrations.RenameModel(
            old_name='CustomerTranportation',
            new_name='CustomerTransportation',
        ),
        migrations.RenameField(
            model_name='staff',
            old_name='staff_job_tUsersitle',
            new_name='staff_job_title',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_order_status',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id_number',
        ),
        migrations.AddField(
            model_name='order',
            name='order_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order_item_cost',
            field=models.IntegerField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_capacity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_paid',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='transporttype',
            name='transport_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='digifarming.TransportCategory'),
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
    ]
