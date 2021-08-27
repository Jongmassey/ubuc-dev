# Generated by Django 3.2.6 on 2021-08-27 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipmentdb', '0004_equipmentfault_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='service',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipmentfault',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='faults', to='equipmentdb.equipment'),
        ),
        migrations.AlterField(
            model_name='equipmentfault',
            name='status',
            field=models.IntegerField(choices=[(0, 'New'), (1, 'In Progress'), (2, 'Fixed'), (3, 'Unfixable'), (4, 'No Fault')]),
        ),
        migrations.AlterField(
            model_name='equipmentservice',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='services', to='equipmentdb.equipment'),
        ),
    ]