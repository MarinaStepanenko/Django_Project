from django.forms import ModelForm, forms
from django.forms.widgets import CheckboxInput, Select

from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "photo", "category", "price")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                # Для чекбоксов (если есть)
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, Select):
                # Для выпадающих списков (категория)
                field.widget.attrs["class"] = "form-select"
            else:
                # Для всех остальных полей (name, description, price, image)
                field.widget.attrs["class"] = "form-control"

            # Добавляем плейсхолдеры
            if field_name == "name":
                field.widget.attrs["placeholder"] = "Введите название товара"
            elif field_name == "description":
                field.widget.attrs["placeholder"] = "Введите описание товара"
                field.widget.attrs["rows"] = 5
            elif field_name == "price":
                field.widget.attrs["placeholder"] = "Введите цену в рублях"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise forms.ValidationError(
                        f"Название содержит запрещенное слово: {word} "
                    )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            desc_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in desc_lower:
                    raise forms.ValidationError(
                        f"Описание содержит запрещенное слово: {word} "
                    )
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is None:
            raise forms.ValidationError(f"Поле 'Цена' обязательно для заполнения")

        if price < 0:
            raise forms.ValidationError(f"'Цена' не может быть отрицательной")

        return price
