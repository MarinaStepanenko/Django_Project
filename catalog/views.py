# from django.shortcuts import render, get_object_or_404
# from django.views.generic import ListView
#
# from catalog.models import Product
#
#
# def home(request):
#     return render(request, "home.html")
#
#
# def contacts(request):
#     return render(request, "contacts.html")
#
#
# def product_list(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, "product_list.html", context)
#
# class ProductListView(ListView):
#     model = Product
#     catalog/product_list.html
#     #app_name/<model_name>_<action>
#
#
# def product_details(request, pk):
#    product = get_object_or_404(Product, pk=pk)
#    context = {"product": product}
#    return render(request, "product_detail.html", context)
from pyexpat.errors import messages

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.core import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from catalog.forms import ProductForm
from catalog.models import Category, Product
from catalog.services import get_products_by_category


class HomeView(TemplateView):
    template_name = "home.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        # 👇 Пробуем получить данные из кеша
        products = cache.get("products_list")

        if products is None:
            # Если в кеше нет — идем в базу данных
            products = Product.objects.filter(is_published=True)
            # 👇 Сохраняем в кеш на 15 минут (900 секунд)
            cache.set("products_list", products, 60 * 15)
            print("🔵 Данные загружены из БД и сохранены в кеш")
        else:
            print("🟢 Данные загружены из кеша")

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # 👈 Передаем категории
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        cache.delete("products_list")
        return super().form_valid(form)


class ProductUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, UpdateView
):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner

    def handle_no_permission(self):
        raise PermissionDenied("Вы не являетесь владельцем продукта")

    def form_valid(self, form):
        product = form.save(commit=False)

        if form.initial.get("is_published", False) and not product.is_published:
            if not self.request.user.has_perm("catalog.can_unpublish_product"):
                form.add_error(
                    "is_published", "У вас нет права снимать продукт с публикации"
                )
                return self.form_invalid(form)

        product.save()
        cache.delete("products_list")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:product_list")
    permission_required = "catalog.delete_product"

    def test_func(self):
        """
        Проверяем, что пользователь может удалить продукт:
        - владелец ИЛИ
        - модератор (имеет право delete_product)
        """
        product = self.get_object()

        # Владелец продукта
        if self.request.user == product.owner:
            return True

        # Модератор
        if self.request.user.has_perm("catalog.delete_product"):
            return True

        return False

    def handle_no_permission(self):
        """Если пользователь не владелец и не модератор"""
        raise PermissionDenied("У вас нет права удалять этот продукт.")

    def form_valid(self, form):
        # Сбрасываем кеш ПЕРЕД удалением
        cache.delete("products_list")
        return super().form_valid(form)


@login_required
@permission_required("catalog.can_unpublish_product", raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not product.is_published:
        messages.warning(request, f"Продукт {product.name} уже снят с публикации")
        return redirect("catalog:product_list")
    product.is_published = False
    product.save()
    cache.delete("products_list")
    messages.success(request, f"Продукт {product.name} снят с публикации")
    return redirect("catalog:product_list")


class CategoryProductsView(
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin, UpdateView
):
    model = Product
    template_name = "catalog/product_category.html"
    context_object_name = "products_category"

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs["pk"])

        return get_products_by_category(self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
