# Generated by Django 4.0.2 on 2023-03-31 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_booking_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.udetails', unique=True),
        ),
    ]
