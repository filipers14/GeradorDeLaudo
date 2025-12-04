from typing import Any


from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView, View

from a_core.forms import FormLaudo, FormRedacao, FormTopico, FormularioDinamico
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
    model = LaudoModelo
    template_name = 'detail.html'
    
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

        return context
    

class ProduzirLaudo(View):

    def get(self, request, pk):
        laudo = get_object_or_404(LaudoModelo, pk=pk)

        topicos_associados = laudo.topicos_associados.all()

        redacoes_associadas =[]
        for topico in topicos_associados:
            redacoes_associadas.extend(topico.redacoes_associadas.all())

        variaveis = set()

        for redacao in redacoes_associadas:
            texto = redacao.texto_redacao
            variaveis.update(self.encontrar_variaveis(texto))

        form = FormularioDinamico(variaveis=variaveis)

        return render(request, 'produzir_laudo.html', {'form': form, 'laudo': laudo})

    def encontrar_variaveis(self, texto):
        import re
        # Usar expressão regular para encontrar as variáveis
        return re.findall(r'<<(\w+)>>', texto)

    