# Generated by Django 4.0.6 on 2022-08-28 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('slot', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SportSpecificSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('court', models.CharField(max_length=50)),
                ('available', models.BooleanField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sports.sport')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sports.slot')),
            ],
        ),
    ]
