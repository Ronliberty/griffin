# Generated by Django 5.1.2 on 2024-10-10 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproject',
            name='status',
            field=models.CharField(choices=[('ongoing', 'Ongoing'), ('completed', 'Completed'), ('on-hold', 'On Hold')], default='ongoing', max_length=20),
        ),
    ]
