# Generated by Django 3.0.3 on 2020-09-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formula_one', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinformation',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contactinformation',
            name='institute_webmail_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contactinformation',
            name='primary_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='contactinformation',
            name='secondary_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddConstraint(
            model_name='contactinformation',
            constraint=models.UniqueConstraint(fields=('entity_content_type', 'primary_phone_number'), name='unique_primary_number'),
        ),
        migrations.AddConstraint(
            model_name='contactinformation',
            constraint=models.UniqueConstraint(fields=('entity_content_type', 'secondary_phone_number'), name='unique_secondary_number'),
        ),
        migrations.AddConstraint(
            model_name='contactinformation',
            constraint=models.UniqueConstraint(fields=('entity_content_type', 'email_address'), name='unique_email_address'),
        ),
        migrations.AddConstraint(
            model_name='contactinformation',
            constraint=models.UniqueConstraint(fields=('entity_content_type', 'institute_webmail_address'), name='unique_institute_webmail_address'),
        ),
    ]
