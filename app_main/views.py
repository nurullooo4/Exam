from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Sum
from django.contrib import messages


from app_main.models import Category, Product, Cart
from app_users.models import Checkout


class HomeView(ListView):
    model = Product
    template_name = 'app_main/home.html'
    context_object_name = 'products'
    paginate_by = 6
    extra_context = {
        'is_home': True
    }

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('images')

        search_query = self.request.GET.get('q', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset


class CategoryView(ListView):
    model = Category
    template_name = 'app_main/category.html'
    context_object_name = 'categories'
    paginate_by = 6
    extra_context = {
        'is_home': True
    }

    def get_queryset(self):
        queryset = Category.objects.all()
        search_query = self.request.GET.get('q', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset


class ProductListView(ListView):
    model = Product
    template_name = 'app_main/product-list.html'
    context_object_name = 'products'
    paginate_by = 6
    pk_url_kwarg = 'category_id'
    extra_context = {
        'is_home': True
    }

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('images')

        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.kwargs.get('category_id')
        if category_id:
            context['category'] = get_object_or_404(Category, id=category_id)

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_main/product-detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['product'] = self.object

        return context


class CartView(ListView):
    model = Cart
    template_name = 'app_main/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = sum(item.total_price for item in context['cart_items'])
        context['total_price'] = total_price
        context['10_days_later'] = date.today() + timedelta(days=10)
        context['today'] = date.today()
        context['total_amount'] = total_price + 10
        return context


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart.quantity += 1
        cart.save()

    return redirect('cart')


def delete_product_cart(request, product_id):
    cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user)

    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')


def add_product_cart(request, product_id, action):
    cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user)

    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif action == 'decrement' and cart_item.quantity == 1:
        cart_item.delete()
        return redirect('cart')

    cart_item.save()

    return redirect('cart')


@login_required
def save_checkout(request):
    if request.method == "POST":
        # Foydalanuvchiga tegishli Checkout modelini olish yoki yaratish
        checkout, created = Checkout.objects.get_or_create(user=request.user)

        # Tanlangan mahsulotlarni olish
        product_ids = request.POST.getlist('product_ids')

        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
            checkout.products.add(*products)

        messages.success(request, 'Your order has been successfully placed!')

        # Savatdagi barcha mahsulotlarni o'chirish
        cart_items = Cart.objects.filter(user=request.user)  # Cart modelini to'g'ri nom bilan almashtiring
        cart_items.delete()  # Cartdagi barcha mahsulotlarni o'chiradi

        return redirect('home')

    return redirect('home')