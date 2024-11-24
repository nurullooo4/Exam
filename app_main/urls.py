from django.urls import path

from app_main import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('categories/', views.CategoryView.as_view(), name='category'),
    path('category-list/<int:category_id>/', views.ProductListView.as_view(), name='category-product-list'),
    path('product-detail/<int:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('delete-product-cart/<int:product_id>/', views.delete_product_cart, name='delete_product_cart'),

    path('add-product-cart/<int:product_id>/<str:action>/', views.add_product_cart, name='add_product_cart'),
    path('checkout-delete/', views.checkout_delete, name='checkout_delete'),
]