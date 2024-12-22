# Generated by Django 4.2.7 on 2024-12-10 00:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prcr", "0006_feature"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="brand",
            field=models.CharField(
                max_length=128,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        2, "Brand name must be longer than two letters."
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="brand",
            name="company",
            field=models.CharField(
                max_length=128,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        2, "Brand name must be longer than two letters."
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="category",
            field=models.CharField(
                max_length=50,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        2, "Category name must be longer than two letters."
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product",
            field=models.CharField(
                max_length=128,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        2, "Product name must be longer than two letters."
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="subcategory",
            name="subcategory",
            field=models.CharField(
                max_length=50,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(
                        2, "Sub-category name must be longer than two letters."
                    )
                ],
            ),
        ),
        migrations.AlterUniqueTogether(
            name="feature",
            unique_together={("feature", "product")},
        ),
    ]