# Generated by Django 4.0 on 2023-09-21 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='access',
            unique_together={('product', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='watchstatus',
            unique_together={('lesson', 'user')},
        ),
    ]
