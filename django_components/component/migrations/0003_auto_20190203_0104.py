# Generated by Django 2.1.5 on 2019-02-03 00:04

from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('component', '0002_auto_20190203_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='kwargs',
            field=picklefield.fields.PickledObjectField(blank=True, editable=False, null=True, verbose_name='keyword arguments'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='comprehensive',
            field=models.ForeignKey(blank=True, help_text='set the comprehensive screen of which this current screen is a specific version of', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specific_set', to='component.Screen', verbose_name='overloaded screen'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='icon',
            field=models.CharField(help_text='icon name, according to your CSS framework - used as visual identification everywhere it should', max_length=16, verbose_name='CSS icon name'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='parent view', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_set', to='component.Screen', verbose_name='parent'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='title',
            field=models.CharField(db_index=True, help_text='used in html head and H1 (you can use templating language)', max_length=127, verbose_name='screen title'),
        ),
    ]