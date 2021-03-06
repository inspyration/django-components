# Generated by Django 2.1.5 on 2019-02-11 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('component', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Browser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='The way the data will be see from foreign objects', max_length=16, unique=True, verbose_name='label')),
                ('condition', models.CharField(blank=True, help_text='The condition expressed as HTML compliant format', max_length=16, null=True, unique=True, verbose_name='condition')),
            ],
            options={
                'verbose_name': 'Browser',
                'verbose_name_plural': 'Browsers',
            },
        ),
        migrations.CreateModel(
            name='HtmlTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='The way the data will be see from foreign objects', max_length=255, unique=True, verbose_name='label')),
            ],
            options={
                'verbose_name': 'Html tag',
                'verbose_name_plural': 'Html tags',
            },
        ),
        migrations.CreateModel(
            name='HttpResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='The way the data will be see from foreign objects', max_length=255, unique=True, verbose_name='label')),
                ('path', models.CharField(blank=True, help_text='Path to the (hosted) resource', max_length=127, verbose_name='path')),
                ('browser', models.ForeignKey(help_text='Specific Browser (potentially with version number)', on_delete=django.db.models.deletion.PROTECT, related_name='browser_httpresource_set', to='template.Browser', verbose_name='browser')),
                ('tag', models.ForeignKey(help_text='HTML Tag used to call this resource', on_delete=django.db.models.deletion.PROTECT, related_name='tag_httpresource_set', to='template.HtmlTag', verbose_name='tag')),
            ],
            options={
                'verbose_name': 'Http resource',
                'verbose_name_plural': 'Http resources',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='The way the data will be see from foreign objects', max_length=255, unique=True, verbose_name='label')),
            ],
            options={
                'verbose_name': 'keyword',
                'verbose_name_plural': 'keywords',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='The way the data will be see from foreign objects', max_length=255, unique=True, verbose_name='label')),
                ('component', models.OneToOneField(blank=True, help_text='If this is null, this menu item is a not a leaf', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='template', to='component.Component', verbose_name='component used by this template')),
                ('keyword_set', models.ManyToManyField(blank=True, related_name='template_set', to='template.Keyword')),
                ('resource_set', models.ManyToManyField(blank=True, related_name='template_set', to='template.HttpResource')),
            ],
            options={
                'verbose_name': 'template',
                'verbose_name_plural': 'templates',
            },
        ),
    ]
