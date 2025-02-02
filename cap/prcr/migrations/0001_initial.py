# Generated by Django 4.2.7 on 2024-12-28 18:42

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
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "brand",
                    models.CharField(
                        max_length=128,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "Brand name must be longer than two letters."
                            )
                        ],
                    ),
                ),
                (
                    "company",
                    models.CharField(
                        max_length=128,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "Brand name must be longer than two letters."
                            )
                        ],
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
            ],
            options={
                "unique_together": {("brand", "company")},
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "Category name must be longer than two letters."
                            )
                        ],
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        validators=[
                            django.core.validators.MinLengthValidator(
                                3, "Comment must be longer than three characters"
                            )
                        ]
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tag",
                    models.CharField(
                        choices=[
                            ("HF", "Hidden fee"),
                            ("HP", "Higher price at checkout"),
                            ("OC", "Overcharge"),
                            ("FI", "Financing"),
                            ("TS", "Tied sale"),
                            ("PS", "Phony sale"),
                        ],
                        default="HF",
                        max_length=2,
                    ),
                ),
                ("description", models.CharField(blank=True, max_length=50)),
                ("added_cost", models.DecimalField(decimal_places=2, max_digits=7)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SubCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subcategory",
                    models.CharField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "Sub-category name must be longer than two letters."
                            )
                        ],
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subcategory_category",
                        to="prcr.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "subcategory",
                "verbose_name_plural": "subcategories",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "product",
                    models.CharField(
                        max_length=128,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                2, "Product name must be longer than two letters."
                            )
                        ],
                    ),
                ),
                ("picture", models.BinaryField(blank=True, editable=True, null=True)),
                (
                    "content_type",
                    models.CharField(
                        blank=True,
                        help_text="The MimeTypeof the file",
                        max_length=256,
                        null=True,
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "brand",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_brand",
                        to="prcr.brand",
                    ),
                ),
                (
                    "comments",
                    models.ManyToManyField(
                        related_name="product_comments",
                        through="prcr.Comment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "subcategory",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_subcategory",
                        to="prcr.subcategory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Price",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("link", models.URLField(max_length=256)),
                ("date_observed", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="price_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="price_product",
                        to="prcr.product",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(related_name="price_tags", to="prcr.tag"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="comment",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="prcr.product"
            ),
        ),
        migrations.CreateModel(
            name="Feature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("feature", models.CharField(max_length=128)),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feature_product",
                        to="prcr.product",
                    ),
                ),
            ],
            options={
                "unique_together": {("feature", "product")},
            },
        ),
    ]
