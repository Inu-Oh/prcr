from django.urls import path
from . import views

app_name = 'prcr'
urlpatterns = [
    # Category list view
    path('', views.CategoryListView.as_view(), name='main_list'),

    # Category and subcategory create views
    path('new_category', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/new_subcategory',
         views.SubcategoryCreateView.as_view(), name='subcategory_create'),

    # Brand create view
    path('new_brand', views.BrandCreateView.as_view(), name='brand_create'),

    # Brand list view
    path('brands', views.BrandListView.as_view(), name='brand_list'),
    # Create product from brand list view
    path('brands/<int:pk>/create_product',
         views.ProductBrandCreateView.as_view(), name='product_brand_create'),

    # Product list view
    path('subcategory/<int:pk>/products', views.ProductListView.as_view(), name='product_list'),
    # Create product from subcategory list view
    path('subcategory/<int:pk>/create_product',
         views.ProductSubcategoryCreateView.as_view(), name='product_subcategory_create'),

    # Product detail, update and add image views
    path('products/<int:pk>/detail', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/add_image', views.ProductAddImageView.as_view(), name='product_add_image'),

    # Feature create view
    path('product/<int:pk>/new_feature', views.FeatureCreateView.as_view(), name='feature_create'),

    # Price create & update view
    path('product/<int:pk>/new_price', views.PriceCreateView.as_view(), name='price_create'),
    path('update_price/<int:pk>', views.PriceUpdateView.as_view(), name='price_update'),

    # Product picture view
    path('picture/<int:pk>', views.stream_file, name='product_picture'),

    # Comment create and delete views
    path('product/<int:pk>/comment', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete',  views.CommentDeleteView.as_view(), name='comment_delete'),

    path('comment/<int:pk>/like', views.LikeCommentView.as_view(), name='like_comment'),
    # path('comment/<int:pk>/dismiss_like', views.DismissLikeView.as_view(), name='dismiss_like'),
]