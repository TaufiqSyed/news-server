# Generated by Django 5.0.6 on 2024-07-12 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_api', '0006_alter_newsarticle_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='url',
            field=models.CharField(max_length=1000, primary_key=True, serialize=False),
        ),
    ]
