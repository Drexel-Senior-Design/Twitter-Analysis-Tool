# Generated by Django 2.2 on 2020-03-14 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag_search',
            name='ml_model',
            field=models.CharField(choices=[('rf', 'Random Forest'), ('nb', 'Naive Bayes'), ('ada', 'Ada Boost'), ('lstm', 'LSTM')], default='rf', max_length=100),
        ),
    ]
