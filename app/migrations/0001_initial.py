# Generated by Django 3.1.7 on 2021-04-26 14:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=5000)),
                ('reviewcount', models.IntegerField(default=0)),
                ('scoretotal', models.BigIntegerField(default=0)),
                ('chapters', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('bookmarks', models.ManyToManyField(blank=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('text', models.CharField(max_length=50000)),
                ('release', models.DateTimeField(auto_now_add=True)),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.book')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('release', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chapter')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.comment')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=100, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('release', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=5000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.book')),
            ],
            options={
                'unique_together': {('author', 'novel')},
            },
        ),
        migrations.CreateModel(
            name='LastRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.book')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chapter')),
            ],
            options={
                'unique_together': {('author', 'book')},
            },
        ),
    ]
