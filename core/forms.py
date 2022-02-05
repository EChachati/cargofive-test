from django import forms
from core.models import Contract


class ContractForm(forms.Form):
    """
    Contract Form to add the excel file with Rates information

    :param name: Name of the contract
    :param date: Date of the contract
    :param file: Excel file with the rates information

    Notes on the fields:
    1. name: CharField, required, minimum 3 characters, max length 100 characters
    2. date: DateField, required
    3. file: FileField, required, must be a valid Excel file

    On the fields is set as required=False, because the validation is made in the clean function,
    otherwise it will display a required error twice when a field is not submitted
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
        """
        This function validates the form and returns the cleaned data
        """
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


class ChoiceContractForm(forms.Form):
    queryset = Contract.objects.all()
    contract_1 = forms.ModelChoiceField(
        queryset,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )
    contract_2 = forms.ModelChoiceField(
        queryset,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        contract_1 = cleaned_data.get('contract_1')
        contract_2 = cleaned_data.get('contract_2')

        if not contract_1:
            self._errors['Contrato 1'] = self.error_class(
                ['El contrato 1 es obligatorio'])
        if not contract_2:
            self._errors['Contrato 2'] = self.error_class(
                ['El contrato 2 es obligatorio'])

        return self.cleaned_data
