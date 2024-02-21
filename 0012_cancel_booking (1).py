# Generated by Django 4.0.2 on 2023-04-09 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_flight_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='cancel_booking',
            fields=[
                ('cancel_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('booking_id', models.IntegerField(verbose_name=200)),
                ('user_id', models.IntegerField(verbose_name=200)),
                ('uname', models.CharField(max_length=200)),
                ('fullname', models.CharField(max_length=200)),
                ('email_id', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zip', models.CharField(max_length=200)),
                ('name_on_card', models.CharField(max_length=200)),
                ('cc_number', models.CharField(max_length=200)),
                ('exp_month', models.CharField(max_length=200)),
                ('exp_yr', models.IntegerField(verbose_name=200)),
                ('cvv', models.IntegerField(verbose_name=200)),
                ('meal', models.IntegerField(verbose_name=200)),
                ('parking', models.IntegerField(verbose_name=200)),
                ('taxcharge', models.IntegerField(verbose_name=200)),
                ('total', models.IntegerField(verbose_name=200)),
                ('roomprice', models.IntegerField(verbose_name=200)),
                ('hotelname', models.CharField(max_length=200)),
                ('checkin_date', models.DateField(null=True)),
                ('checkout_date', models.DateField(null=True)),
            ],
        ),
    ]
