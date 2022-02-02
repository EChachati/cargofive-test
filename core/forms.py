from django.forms import Form
from django.core.validators import FileExtensionValidator
from core.models import Contracts


class ContractForm(Form):
    """
    """
    name = forms.CharField(max_length=100)
    date = forms.DateField()
    file = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['xlsx']
            )
        ]
    )
