from typing import Any


from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView

from a_core.forms import FormLaudo, FormRedacao, FormTopico
from a_core.models import *

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

class CriarRedacaoModelo(CreateView):
    model = RedacaoModelo
    template_name = 'form.html'
    form_class = FormRedacao
    success_url = reverse_lazy('a_core:lista_redacao_modelo')

class DetalhesRedacaoModelo(DetailView):
    model = RedacaoModelo
    template_name = 'detail.html'

class EditarRedacaoModelo(UpdateView):
    model = RedacaoModelo
    form_class = FormRedacao
    template_name = 'form.html'
    success_url = reverse_lazy('a_core:lista_redacao_modelo')

class ListaRedacaoModelo(ListView):
    model = RedacaoModelo
    template_name = 'list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['criar_url'] = 'a_core:criar_redacao_modelo'
        context['label_criar'] = 'Criar Redação'
        context['editar_url'] = 'a_core:editar_redacao_modelo'
        return context

class CriarTopicoModelo(CreateView):
    model = TopicoModelo
    template_name = 'form.html'
    form_class = FormTopico
    success_url = reverse_lazy('a_core:lista_topico_modelo')

class DetalhesTopicoModelo(DetailView):
    pass

class EditarTopicoModelo(UpdateView):
    model = TopicoModelo
    form_class = FormTopico
    template_name = 'form.html'
    success_url = reverse_lazy('a_core:lista_topico_modelo')


class ListaTopicoModelo(ListView):
    model = TopicoModelo
    template_name = 'list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['criar_url'] = 'a_core:criar_topico_modelo'
        context['label_criar'] = 'Criar Tópico'
        context['editar_url'] = 'a_core:editar_topico_modelo'
        return context


class CriarLaudoModelo(CreateView):
    model = LaudoModelo
    form_class = FormLaudo
    template_name = 'form.html'
    success_url = reverse_lazy('a_core:lista_laudo_modelo')

class DetalhesLaudoModelo(DetailView):
    pass

class EditarLaudoModelo(UpdateView):
    model = LaudoModelo
    form_class = FormLaudo
    template_name = 'form.html'
    success_url = reverse_lazy('a_core:lista_laudo_modelo')

class ListaLaudoModelo(ListView):
    model = LaudoModelo
    template_name = 'list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['criar_url'] = 'a_core:criar_laudo_modelo'
        context['label_criar'] = 'Criar Laudo'
        context['editar_url'] = 'a_core:editar_laudo_modelo'

        # INSERT_YOUR_CODE
        # Para cada laudo em object_list, coletar os tópicos e redações associadas
        laudo_topicos = {}
        laudo_redacoes = {}
        for laudo in context.get('object_list', []):
            topicos = laudo.topicos_associados.all()
            redacoes = laudo.redacoes_associadas.all()
            laudo_topicos[laudo.pk] = topicos
            laudo_redacoes[laudo.pk] = redacoes
        context['laudo_topicos'] = laudo_topicos
        context['laudo_redacoes'] = laudo_redacoes
        return context
    


    