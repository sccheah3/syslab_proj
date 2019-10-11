# Generated by Django 2.2.2 on 2019-10-10 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motherboard_model', models.CharField(max_length=200)),
                ('processor_info', models.CharField(max_length=300)),
                ('processor_freq', models.CharField(max_length=200)),
                ('processor_count', models.IntegerField(default=0)),
                ('total_core_count', models.IntegerField(default=0)),
                ('total_dimm_count', models.IntegerField(default=0)),
                ('num_dimm_slots', models.IntegerField(default=0)),
                ('dimm_slots_per_channel', models.IntegerField(default=0)),
                ('dimm_clock_speed', models.CharField(max_length=200)),
                ('dimm_memory_size', models.CharField(max_length=200)),
                ('processor_family', models.CharField(max_length=300)),
                ('hpl_block_size', models.IntegerField(default=0)),
                ('hpl_problem_size', models.IntegerField(default=0)),
                ('linpack_theoretical_score', models.CharField(max_length=300)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('date_modified', models.DateTimeField(verbose_name='date modified')),
            ],
        ),
        migrations.CreateModel(
            name='DIMM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=400)),
                ('part_number', models.CharField(max_length=350)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_test_app.System')),
            ],
        ),
    ]
