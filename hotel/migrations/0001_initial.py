# Generated by Django 5.0.7 on 2024-07-14 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('rooms', models.IntegerField()),
                ('photo', models.ImageField(upload_to='hotel/media/images')),
                ('ratings', models.DecimalField(decimal_places=2, max_digits=3)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=256)),
                ('postcode', models.IntegerField()),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='hotel.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='hotel.hotel')),
            ],
        ),
    ]
