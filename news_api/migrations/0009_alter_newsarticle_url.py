# Generated by Django 5.0.6 on 2024-07-12 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_api', '0008_alter_newsarticle_author_alter_newsarticle_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='url',
            field=models.CharField(max_length=10000, primary_key=True, serialize=False),
        ),
    ]
