from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, HomeView, ContactsView, ProductDetailView

app_name = CatalogConfig.name

print("catalog/urls.py ЗАГРУЖЕН!")

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("product/create/", views.ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update", views.ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete", views.ProductDeleteView.as_view(), name="product_delete"),
]
