from django import Form 
from .models import ProductFeature

class ProductFeatureForm(forms.ModelForm):
    class Meta:
        model = ProductFeature
        fields = ["product", "key", "Value"]
