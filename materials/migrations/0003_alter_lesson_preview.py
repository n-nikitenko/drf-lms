# Generated by Django 4.2.15 on 2024-08-14 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0002_alter_course_description_alter_course_preview_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="preview",
            field=models.ImageField(
                blank=True, null=True, upload_to="", verbose_name="Превью"
            ),
        ),
    ]
