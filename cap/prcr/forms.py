from django import forms
from prcr.models import Feature, Product, Price, SubCategory
from django.core.files.uploadedfile import InMemoryUploadedFile
from prcr.humanize import naturalsize


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=250, min_length=3, strip=True)


class FeatureCreateForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['feature']


class PriceCreateForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['price', 'link']


class SubcategoryCreateForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['subcategory']


class ProductBrandCreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Product
        fields = ['product', 'subcategory', 'picture']  # Picture is manual

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(ProductBrandCreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance


class ProductSubcategoryCreateForm(ProductBrandCreateForm):
    class Meta:
        model = Product
        fields = ['product', 'brand', 'picture']


class ProductUpdateForm(ProductBrandCreateForm):
    class Meta:
        model = Product
        fields = ['product', 'brand', 'subcategory', 'picture']


class ProductAddImageForm(ProductBrandCreateForm):
    class Meta:
        model = Product
        fields = ['picture']


# Source: https://www.dj4e.com/lessons/dj4e_ads1b
# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/4.2/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
