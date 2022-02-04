from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new/', ContractFormView.as_view()),
    path('contract/<int:pk>/', TableContractView.as_view()),
    path('', ListContractView.as_view()),
    path('compare/', CompareContractView.as_view()),
]
