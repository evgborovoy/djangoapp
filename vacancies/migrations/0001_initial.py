# Generated by Django 4.2.9 on 2024-01-29 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=60)),
                ('text', models.CharField(max_length=1500)),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('open', 'Открыта'), ('closed', 'Закрыта')], default='draft', max_length=6)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
