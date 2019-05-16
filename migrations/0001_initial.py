import django.core.validators
import django.db.models.deletion
import django_countries.fields
import swapper
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # Depends on the app auth for defining the model User
        swapper.dependency('auth', 'User'),
    ]

    operations = [
        # Generics
        migrations.CreateModel(
            name='ContactInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('primary_phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('secondary_phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('email_address', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('email_address_verified', models.BooleanField(default=False)),
                ('institute_webmail_address', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('entity_object_id', models.PositiveIntegerField()),
                ('video_conference_id', models.CharField(blank=True, max_length=127, null=True, unique=True, verbose_name='video conference ID')),
                ('entity_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'contact information',
            },
        ),
        migrations.CreateModel(
            name='LocationInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=127)),
                ('state', models.CharField(max_length=127)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('postal_code', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{3,9}$'), django.core.validators.MinValueValidator(0)])),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('entity_object_id', models.PositiveIntegerField()),
                ('entity_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'location information',
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('site', models.CharField(choices=[('beh', 'Behance'), ('blo', 'Blogger'), ('dri', 'Dribbble'), ('fac', 'Facebook'), ('fli', 'Flickr'), ('git', 'GitHub'), ('goo', 'Google'), ('lin', 'LinkedIn'), ('med', 'Medium'), ('pin', 'Pinterest'), ('red', 'Reddit'), ('sky', 'Skype'), ('sna', 'Snapchat'), ('tum', 'Tumblr'), ('twi', 'Twitter'), ('you', 'YouTube'), ('oth', 'Other website')], max_length=7)),
                ('url', models.URLField(max_length=255, verbose_name='URL')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('entity_object_id', models.PositiveIntegerField()),
                ('entity_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('links', models.ManyToManyField(blank=True, to='formula_one.SocialLink')),
            ],
            options={
                'verbose_name_plural': 'social information',
            },
        ),
    ]
