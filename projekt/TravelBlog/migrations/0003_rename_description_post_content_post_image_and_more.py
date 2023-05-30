# Generated by Django 4.2.1 on 2023-05-29 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelBlog', '0002_rename_content_post_description_remove_post_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='description',
            new_name='content',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='img/bora_bora.png', upload_to='post_images/'),
        ),
        migrations.AddField(
            model_name='post',
            name='short_description',
            field=models.TextField(default=''),
        ),
    ]