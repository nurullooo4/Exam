from django.contrib import admin

from app_main.models import Product, Category, ProductImage, Cart


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    save_on_top = True
    list_per_page = 3


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity']
    list_display_links = ['id', 'product']
