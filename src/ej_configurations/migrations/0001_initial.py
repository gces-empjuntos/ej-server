# Generated by Django 2.0 on 2018-05-19 12:35

from django.db import migrations, models
import django.db.models.deletion
import ej_configurations.validators
import ej_conversations.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Color name')),
                ('hex_value', models.CharField(help_text='Color code in hex (e.g., #RRGGBBAA) format.', max_length=30, validators=[ej_conversations.validators.validate_color], verbose_name='Color')),
            ],
        ),
        migrations.CreateModel(
            name='Fragment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Unique identifier for fragment name', max_length=100, unique=True, verbose_name='Name')),
                ('format', models.CharField(choices=[('html', 'HTML'), ('md', 'Markdown')], max_length=4)),
                ('content', models.TextField(blank=True, help_text='Raw fragment content in HTML or Markdown', verbose_name='content')),
                ('editable', models.BooleanField(default=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='FragmentLock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fragment', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='lock_ref', to='ej_configurations.Fragment')),
            ],
        ),
        migrations.CreateModel(
            name='SocialMediaIcon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_network', models.CharField(help_text='Name of the social network (e.g., Facebook)', max_length=50, unique=True, verbose_name='Social network')),
                ('icon_name', models.CharField(help_text='Icon name in font-awesome', max_length=50, validators=[ej_configurations.validators.validate_icon_name], verbose_name='Icon name')),
                ('index', models.PositiveSmallIntegerField(help_text='You can manually define the ordering that each icon should appear in the interface. Otherwise, icons will be shown in insertion order.', verbose_name='Ordering')),
                ('url', models.URLField(help_text='Link to your social account page.', verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Social media icon',
                'verbose_name_plural': 'Social media icons',
                'ordering': ['index', 'id'],
            },
        ),
    ]
