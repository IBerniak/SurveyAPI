# Generated by Django 3.2.7 on 2021-09-20 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='givenanswer',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys.question'),
        ),
        migrations.AlterField(
            model_name='completedsurvey',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='surveys.survey'),
        ),
        migrations.AlterField(
            model_name='givenanswer',
            name='answer',
            field=models.TextField(),
        ),
    ]