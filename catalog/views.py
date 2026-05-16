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

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


class HomeView(TemplateView):
    template_name = "home.html"


class ContactsView(TemplateView):
    template_name = "contacts.html"


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_details.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy('catalog:product_list')
