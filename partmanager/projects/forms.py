from django import forms
from .models import BOM


class BOMImportForm(forms.ModelForm):
    bom_file = forms.FileField()

    class Meta:
        model = BOM
        fields = ['name', 'multiply', 'description', 'project', 'bom_file']
