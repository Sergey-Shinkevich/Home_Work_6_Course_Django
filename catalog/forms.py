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