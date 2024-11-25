# Generated by Django 5.1.2 on 2024-11-06 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psusphere', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='college',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='psusphere.college'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='psusphere.college'),
        ),
        migrations.AlterField(
            model_name='orgmember',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psusphere.organization'),
        ),
        migrations.AlterField(
            model_name='orgmember',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psusphere.student'),
        ),
        migrations.AlterField(
            model_name='program',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psusphere.college'),
        ),
        migrations.AlterField(
            model_name='student',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psusphere.program'),
        ),
    ]
