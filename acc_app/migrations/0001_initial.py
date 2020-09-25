from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(
                    max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(
                    blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                               related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='MerchantAccount',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('shop_name', models.CharField(blank=True, max_length=50)),
                ('phone_num', models.BigIntegerField(blank=True, unique=True)),
                ('phone_num2', models.BigIntegerField()),
                ('aadhar', models.BigIntegerField(blank=True, unique=True)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('pincode', models.BigIntegerField(default=0)),
                ('shop_established_date', models.DateField(blank=True, null=True)),
                ('about_shop', models.CharField(blank=True, max_length=200)),
                ('shop_img', models.ImageField(blank=True, upload_to='ShopsIMG')),
                ('shop_type', models.CharField(default='Retailer', max_length=15)),
                ('gst_num', models.BigIntegerField(blank=True)),
                ('available_services', models.CharField(
                    blank=True, max_length=200)),
                ('average_price', models.BigIntegerField(default=0)),
                ('email', models.OneToOneField(
                    on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
