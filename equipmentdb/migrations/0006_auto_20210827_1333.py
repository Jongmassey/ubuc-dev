# Generated by Django 3.2.6 on 2021-08-27 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('equipmentdb', '0005_auto_20210827_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='testtype_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='testtype_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='test',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='test',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='equipmenttypeserviceschedule',
            name='service',
        ),
        migrations.RemoveField(
            model_name='equipmenttypetestschedule',
            name='test',
        ),
        migrations.AddField(
            model_name='equipmentservice',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='equipmentservice',
            name='name',
            field=models.CharField(default='foo', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipmentservice',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipmenttest',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tests', to='equipmentdb.equipment'),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='equipmenttest',
            name='test_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='equipmentdb.testtype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipmenttypetestschedule',
            name='test_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, to='equipmentdb.testtype'),
            preserve_default=False,
        ),
    ]
