# Generated by Django 3.2.5 on 2024-05-31 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='query',
            field=models.CharField(default='leQuery', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('reviewer', 'query'), name='unique_reviewer_query'),
        ),
    ]
