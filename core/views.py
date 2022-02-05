from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.views.generic.base import TemplateView

from core.forms import ContractForm
from core.models import Contract, Rate

from core.utils import read_excel_data, compare_last_two_files


class ContractFormView(FormView):
    """
    Contract Form to add the excel file with Rates information

    Form parameters:
    :param name: Name of the contract
    :param date: Date of the contract
    :param file: Excel file with the rates information
    """
    template_name = 'core/contract_form.html'
    form_class = ContractForm
    success_url = 'new/'

    def form_valid(self, form):
        """
        Gets the form data and creates the Contract object, then calls the
        read_excel_data function to create the Rate objects
        If the form is valid, it redirects to the success_url which shows the
        Contract detail
        """

        file = form.cleaned_data['file'].file
        name = form.cleaned_data['name']
        date = form.cleaned_data['date']

        contract = Contract(name=name, date=date)
        contract.save()
        read_excel_data(file, contract)

        self.success_url = '/contract/{}/'.format(contract.id)

        return super().form_valid(form)


class TableContractView(TemplateView):
    """
    Shows the data of a contract and the rates related to it
    """
    template_name = 'core/contract_table.html'
    queryset = Contract.objects.all()
    context_object_name = 'contract'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rates'] = Rate.objects.filter(contract=context['pk'])
        context['contract'] = Contract.objects.get(pk=context['pk'])
        return context


class ListContractView(ListView):
    """
    Shows all the contracts in a list ordered by date of the contract
    paginate_by: number of contracts per page
    """
    template_name = 'core/contract_list.html'
    model = Contract
    context_object_name = 'contracts'
    ordering = '-date'
    paginate_by = 15


class CompareContractView(TemplateView):
    """
    Shows the difference between the last two contracts
    """
    template_name = 'core/contract_compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract_1'], context['contract_2'], context['routes'], context['changed_items'] = compare_last_two_files()
        return context
