# Generated by Django 2.1.7 on 2019-05-29 16:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('remider', '0002_lasttriggerset'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriggerTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
            ],
        ),
    ]