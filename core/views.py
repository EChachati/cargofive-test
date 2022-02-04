from django.shortcuts import render
from django.views.generic import FormView, ListView
from django.views.generic.base import TemplateView

from core.forms import ContractForm
from core.models import Contract, Rate

from core.utils import read_excel_data, compare_last_two_files


class ContractFormView(FormView):
    """
    Contract Form to add the excel file with Rates information
    """
    template_name = 'core/contract_form.html'
    form_class = ContractForm
    success_url = 'new/'

    def form_valid(self, form):
        file = form.cleaned_data['file'].file
        name = form.cleaned_data['name']
        date = form.cleaned_data['date']

        contract = Contract(name=name, date=date)
        contract.save()
        read_excel_data(file, contract)

        self.success_url = '/contract/{}/'.format(contract.id)

        return super().form_valid(form)


class TableContractView(TemplateView):
    template_name = 'core/contract_table.html'
    queryset = Contract.objects.all()
    context_object_name = 'contract'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rates'] = Rate.objects.filter(contract=context['pk'])
        return context


class ListContractView(ListView):
    template_name = 'core/contract_list.html'
    model = Contract
    context_object_name = 'contracts'
    ordering = '-date'
    paginate_by = 15


class CompareContractView(TemplateView):
    template_name = 'core/contract_compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = compare_last_two_files()
        import pdb
        #pdb.set_trace()
        return context
