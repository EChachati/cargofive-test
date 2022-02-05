from django import forms
from core.models import Contract


class ContractForm(forms.Form):
    """
    Contract Form to add the excel file with Rates information
    """
    name = forms.CharField(
        max_length=100,
        label='Nombre',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'placeholder': 'Nombre',
                'id': 'name',
                'class': 'form-control',
            }
        ),
        required=False
    )

    date = forms.DateField(
        label='Fecha',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'id': 'date',
                'class': 'form-control'
            }
        ),
        required=False
    )
    file = forms.FileField(
        label='Archivo',
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'id': 'file',
                'class': 'form-control'
            }
        ),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        date = cleaned_data.get('date')
        file = cleaned_data.get('file')

        if not name:
            self._errors['Nombre'] = self.error_class(
                ['El nombre es obligatorio'])
        if name and len(name) < 3:
            self._errors['Nombre'] = self.error_class(
                ['El nombre debe tener al menos 3 caracteres'])
        if not date:
            self._errors['Fecha'] = self.error_class(
                ['La fecha es obligatoria'])
        if not file:
            self._errors['Archivo'] = self.error_class(
                ['El archivo es obligatorio'])

        if file and not file.name.endswith('xlsx'):
            self._errors['Archivo'] = self.error_class(
                ['El archivo debe ser un archivo de excel'])

        return self.cleaned_data
