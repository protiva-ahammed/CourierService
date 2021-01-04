# Generated by Django 3.1.4 on 2020-12-17 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0010_customer_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=200, null=True)),
                ('contract', models.CharField(max_length=11, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('payment', models.FloatField(null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Complited', 'Complited'), ('Delivered', 'Delivered')], max_length=200, null=True)),
                ('receiver', models.CharField(max_length=200, null=True)),
                ('phn', models.CharField(max_length=11, null=True)),
                ('destination', models.CharField(choices=[('Dhaka', 'Dhaka'), ('Rajshahi', 'Rajshahi'), ('Bogura', 'Bogura'), ('Chittagong', 'Chittagong'), ('Syllet', 'Syllet')], max_length=200, null=True)),
                ('packing', models.CharField(choices=[('Envelope', 'Envelop'), ('Cardboard', 'Cardboard'), ('Paperboard', 'Paperboard'), ('PlasticBox', 'PlasticBox'), ('RigidBoxes', 'RigidBoxes')], max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='download.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]