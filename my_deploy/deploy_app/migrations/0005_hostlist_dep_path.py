# Generated by Django 4.0.5 on 2022-07-01 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_app', '0004_hostlist_des_path_delete_deployhost'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostlist',
            name='dep_path',
            field=models.CharField(max_length=200, null=True, verbose_name='部署路径'),
        ),
    ]
