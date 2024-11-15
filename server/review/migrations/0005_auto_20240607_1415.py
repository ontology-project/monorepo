# Generated by Django 3.2.5 on 2024-06-07 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_alter_review_rating'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_reviewer_query',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('reviewer', 'query', 'curriculum'), name='unique_reviewer_query_curriculum'),
        ),
    ]
