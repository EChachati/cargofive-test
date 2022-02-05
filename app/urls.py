from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
        name='admin'
    ),
    path(
        'new/',
        ContractFormView.as_view(),
        name='new'
    ),
    path(
        'contract/<int:pk>/',
        TableContractView.as_view(),
        name='contract_detail'
    ),
    path(
        '',
        ListContractView.as_view(),
        name='list'
    ),
    path(
        'compare/',
        CompareContractView.as_view(),
        name='compare'
    ),
]
