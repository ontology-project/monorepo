# Generated by Django 3.2.5 on 2024-05-31 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20240531_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='curriculum',
            field=models.CharField(default='leCurriculum', max_length=1000),
            preserve_default=False,
        ),
    ]
