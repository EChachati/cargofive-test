from django import forms
from django.core.validators import FileExtensionValidator
from core.models import Contract


class ContractForm(forms.Form):
    """
    Contract Form to add the excel file with Rates information
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        label='Nombre',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'placeholder': 'Nombre'
            }
        )
    )
    date = forms.DateField(
        required=True,
        label='Fecha',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    file = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['xlsx']
            )
        ],
        label='Archivo'
    )
