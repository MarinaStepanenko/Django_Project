from django import forms


class StyleFormMixin:
    """
    Миксин для автоматического добавления CSS-классов ко всем полям формы.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Пропускаем скрытые поля и поля с файлами
            if isinstance(field.widget, forms.HiddenInput):
                continue
            if isinstance(field.widget, forms.FileInput):
                continue

            # Добавляем класс 'form-control' ко всем полям
            if hasattr(field.widget, "attrs"):
                field.widget.attrs["class"] = (
                    field.widget.attrs.get("class", "") + " form-control"
                )

                # Для полей с ошибками добавляем дополнительный класс
                if self.errors.get(field_name):
                    field.widget.attrs["class"] += " is-invalid"
