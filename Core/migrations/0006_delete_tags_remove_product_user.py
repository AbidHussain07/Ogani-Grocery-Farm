# Generated by Django 5.0.8 on 2024-08-23 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0005_alter_product_vendor'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tags',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
    ]
