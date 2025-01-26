from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
# from django.contrib.auth.models import User
from django.conf import settings

from decimal import Decimal

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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Like',
        related_name='liked_comments')
    likes_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Snippet
    def __str__(self):
        if len(self.text) < 17:
            return self.text
        return self.text[:13] + '...'


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='like_users')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return '%s likes %s'%(self.user.username, self.comment.text[:9])


class Price(models.Model):
    advertised_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="The initial price you saw for the product"
    )
    shipping = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0.0,
        help_text="Added cost for shipping."
    )
    hidden_fees = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0.0,
        help_text="Fees added to the advertised price before checkout, except shipping."
    )
    higher_price_at_checkout = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0.0,
        help_text="The price charged at checkout, if it was higher. Leave 0.0 otherwise. Don't apply hidden fees."
    )
    overcharge = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0.0,
        help_text="The overcharge price on your card, if higher than at checkout. Leave 0.0 otherwise. Don't apply hidden fees."
    )
    tied_sale = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0.0,
        help_text="Add the price of other products you had to buy in order to get the product at advertised price."
        )
    total = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0.0,
        help_text="Total cost of final product price and all fees."
        )
    tied_cost = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=0.0,
        help_text="Cost of buying all bundled products."
        )
    financing = models.BooleanField(default=False,
        help_text="Must buy financing to get product at advertised price.")
    subscription_fees = models.BooleanField(default=False,
        help_text="Price is conditional on subscription or subscription fees may apply.")
    phony_sale = models.BooleanField(default=False,
        help_text="The store lied about how much you saved on the product.")

    comments = models.CharField(max_length=128, blank=True,
        help_text="Describe any misleading pricing claims.")
    link = models.URLField(max_length=256)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_product")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        related_name="price_owner")

    date_observed = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        price_str = str(self.advertised_price) + " (on " + str(self.date_observed) + ")"
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