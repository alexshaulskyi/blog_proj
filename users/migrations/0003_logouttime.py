# Generated by Django 3.0.7 on 2020-06-25 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogoutTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logout', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logout_time', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
