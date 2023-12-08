# Generated by Django 4.2.1 on 2023-12-08 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_courier_order_created_at_order_updated_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='representative_name',
            new_name='representative_full_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='representative_surname',
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='giorgi tarsaidze', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('DF', 'DEFAULT'), ('GR', 'GREEN'), ('YL', 'YELLOW'), ('RD', 'RED'), ('BK', 'BLACK')], default='DF', max_length=2),
        ),
    ]
