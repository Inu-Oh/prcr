from django.db import models
from django.core.validators import MinLengthValidator
# from django.contrib.auth.models import User
from django.conf import settings

# from taggit.managers import TaggableManageer # need to install and add to settings

class Category(models.Model):
    category = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, "Category name must be longer than two letters.")],
        unique=True,
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.category

    class Meta:
        verbose_name_plural = "categories"


class SubCategory(models.Model):
    subcategory = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2, "Sub-category name must be longer than two letters.")],
        unique=True,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
        related_name="subcategory_category")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.subcategory

    class Meta:
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"


class Brand(models.Model):
    brand = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(2, "Brand name must be longer than two letters.")],
        unique=True,
    )
    company = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(2, "Brand name must be longer than two letters.")]
    )
    class Meta:
        unique_together = ['brand', 'company']
    # add logo for upload
    # add trust rating
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        if self.company:
            return self.brand + " (" + self.company + ")"
        else:
            return self.brand


class Product(models.Model):
    product = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(2, "Product name must be longer than two letters.")],
        unique=True,
    )
    brand = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL,
        related_name="product_brand")
    subcategory = models.ForeignKey(SubCategory, null=True, on_delete=models.SET_NULL,
        related_name="product_subcategory")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        related_name="product_owner")
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='product_comments')

    # Picture upload
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, blank=True,
        help_text='The MimeTypeof the file')


    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        product_str = self.product
        if self.brand and self.subcategory:
            product_str = product_str + " by " + self.brand.brand + " (" + self.subcategory.category.category + ")"
        elif self.brand:
            product_str = product_str + " by " + self.brand.brand
        elif self.subcategory:
            product_str = product_str + " (" + self.subcategory.subcategory + ", " + self.subcategory.category.category + ")"
        return product_str


class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be longer than three characters")]
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Snippet
    def __str__(self):
        if len(self.text) < 17:
            return self.text
        return self.text[:13] + '...'


class Price(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=256)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_product")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        related_name="price_owner")

    date_observed = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        price_str = str(self.price) + " (on " + str(self.date_observed) + ")"
        return price_str


class Feature(models.Model):
    feature = models.CharField(max_length=128)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="feature_product")
    class Meta:
        unique_together = ['feature', 'product']

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.feature