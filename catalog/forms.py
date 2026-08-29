from django import forms
from .models import Product

FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):

  class Meta:
    model = Product
    fields = [
        'name',
        'description',
        'image',
        'category',
        'purchase_price',
    ]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Настраиваем стили в зависимости от типа виджета поля
    for field_name, field in self.fields.items():
      if isinstance(field.widget, forms.CheckboxInput):
        # Для чекбоксов
        field.widget.attrs['class'] = 'form-check-input'
      elif isinstance(field.widget, forms.ClearableFileInput):
        # Для поля загрузки файлов/изображений
        field.widget.attrs['class'] = 'form-control-file'
      else:
        # Для текста, текстовых областей и селектов
        field.widget.attrs['class'] = 'form-control'

  def _validate_forbidden_words(self, value):
    if not value:
      return value
    value_lower = value.lower()
    for word in FORBIDDEN_WORDS:
      if word in value_lower:
        raise forms.ValidationError(
            f'Использование слова или части слова «{word}» запрещено.'
        )
    return value

  def clean_name(self):
    return self._validate_forbidden_words(self.cleaned_data.get('name'))

  def clean_description(self):
    return self._validate_forbidden_words(
        self.cleaned_data.get('description')
    )

  def clean_purchase_price(self):
    price = self.cleaned_data.get('purchase_price')
    if price is not None and price < 0:
      raise forms.ValidationError('Цена продукта не может быть отрицательной.')
    return price