from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_details

app_name = CatalogConfig.name

print("catalog/urls.py ЗАГРУЖЕН!")

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("products/", views.product_list, name="product_list"),
    path("products/<int:pk>", product_details, name="product_details" )
]
