# -*- coding: utf-8 -*-
import django_filters
from .models import *
from django_filters import *
from django import forms
class UserFilter(django_filters.FilterSet):
    forma_pagamento = ChoiceFilter(choices=pagamentos, widget=forms.RadioSelect)
    class Meta:
        model = Conta
        fields = ['status_pag']