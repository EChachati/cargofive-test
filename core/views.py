from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from core.forms import ContractForm
from core.models import Contract

from core.utils import read_excel_data


class ContractFormView(FormView):
    """
    Contract Form to add the excel file with Rates information
    """
    template_name = 'core/contract_form.html'
    form_class = ContractForm
    success_url = '/'

    def form_valid(self, form):
        file = form.cleaned_data['file'].file
        name = form.cleaned_data['name']
        date = form.cleaned_data['date']

        contract = Contract(name=name, date=date)
        contract.save()

        read_excel_data(file, contract)

        return super().form_valid(form)
