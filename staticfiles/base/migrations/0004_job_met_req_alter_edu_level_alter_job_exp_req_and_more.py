# Generated by Django 4.2 on 2023-04-23 13:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_job_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='met_req',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='edu',
            name='level',
            field=models.CharField(choices=[('basic', 'basic'), ('higher', 'higher'), ('graduation', 'graduation'), ('post graduation', 'post graduation'), ('doctorate', 'doctorate'), ('certifications', 'certifications')], default='graduation', max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='exp_req',
            field=models.IntegerField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 23, 18, 52, 56, 852236)),
        ),
    ]
