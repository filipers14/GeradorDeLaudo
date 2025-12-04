from typing import Any

from django.shortcuts import redirect
from django.forms import inlineformset_factory

from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView, View, DeleteView

from a_core.forms import *
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
    '''
    Cria o Laudo Modelo e, ao salvar, armazena as variáveis encontradas nas redações associadas dos tópicos e as redacoes_associadas diretamente no modelo VariaveisModelo, se ainda não existirem.
    '''
    model = LaudoModelo
    form_class = FormLaudo
    template_name = 'form.html'
    success_url = reverse_lazy('a_core:lista_laudo_modelo')

    def form_valid(self, form):
        import re
        response = super().form_valid(form)

        laudo = self.object  # LaudoModelo já salvo pelo super().form_valid()

        # Armazena todas as variáveis que já existiram para evitar duplicatas no banco
        variaveis_existem = set(
            v.nome_variavel for v in VariaveisModelo.objects.all()
        )

        # Função para extrair variáveis de um texto de redação
        def encontrar_variaveis(texto):
            return re.findall(r'<<(\w+)>>', texto)

        # Percorre os tópicos associados e suas redações
        for topico in laudo.topicos_associados.all():
            for redacao in topico.redacoes_associadas.all():
                variaveis = encontrar_variaveis(redacao.texto_redacao)
                for nome_var in variaveis:
                    if nome_var not in variaveis_existem:
                        VariaveisModelo.objects.create(
                            nome_variavel=' '.join(word.capitalize() for word in nome_var.split('_')),
                            string_substituicao=nome_var,
                            tipo_campo='Campo Aberto',  # ou algum padrão desejado
                            status='ativo',
                            laudo_associado=laudo
                        )
                        variaveis_existem.add(nome_var)
        # Também verificar as redacoes_associadas diretamente ao laudo (caso esteja usando esse m2m)
        for redacao in laudo.redacoes_associadas.all():
            variaveis = encontrar_variaveis(redacao.texto_redacao)
            for nome_var in variaveis:
                if nome_var not in variaveis_existem:
                    VariaveisModelo.objects.create(
                        nome_variavel=' '.join(word.capitalize() for word in nome_var.split('_')),
                        string_substituicao='',
                        tipo_campo='Campo Aberto',
                        status='ativo',
                        laudo_associado=laudo
                    )
                    variaveis_existem.add(nome_var)

        return response

class DetalhesLaudoModelo(DetailView):
    model = LaudoModelo
    template_name = 'detail.html'
    
class EditarLaudoModelo(UpdateView):
    model = LaudoModelo
    form_class = FormLaudo
    template_name = 'form.html'
    success_url = reverse_lazy('a_core:lista_laudo_modelo')

class DeletarLaudoModelo(DeleteView):
    model = LaudoModelo
    success_url = reverse_lazy('a_core:lista_laudo_modelo')
    template_name = 'blank.html'  # Não usaremos o template

    def get(self, request, *args, **kwargs):
        # Realiza o delete diretamente em uma requisição GET (sem confirmação).
        return self.post(request, *args, **kwargs)

    def get_template_names(self):
        # Não renderiza nenhum template.
        return []

class ListaLaudoModelo(ListView):
    model = LaudoModelo
    template_name = 'list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['criar_url'] = 'a_core:criar_laudo_modelo'
        context['label_criar'] = 'Criar Laudo'
        context['editar_url'] = 'a_core:editar_laudo_modelo'

        return context
    
class EditarVariavelModelo(UpdateView):
    model = VariaveisModelo
    template_name = 'form.html'
    form_class = FormVariavel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ValorVariavelFormSet = inlineformset_factory(
            VariaveisModelo,
            ValorVariavelModelo,
            fields=('valor_variavel', 'status'),
            extra=1,
            can_delete=True
        )

        if self.request.method == 'POST':
            formset = ValorVariavelFormSet(self.request.POST, instance=self.object)
        else:
            formset = ValorVariavelFormSet(instance=self.object)
        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            laudo_pk = self.object.laudo_associado.pk
            return redirect('a_core:detalhes_laudo_modelo', pk=laudo_pk)
        else:
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data(**kwargs)
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        laudo_pk = self.object.laudo_associado.pk
        return reverse_lazy('a_core:detalhes_laudo_modelo', kwargs={'pk': laudo_pk})


# class ProduzirLaudo(View):

#     def get(self, request, pk):
#         laudo = get_object_or_404(LaudoModelo, pk=pk)

#         topicos_associados = laudo.topicos_associados.all()

#         redacoes_associadas =[]
#         for topico in topicos_associados:
#             redacoes_associadas.extend(topico.redacoes_associadas.all())

#         variaveis = set()

#         for redacao in redacoes_associadas:
#             texto = redacao.texto_redacao
#             variaveis.update(self.encontrar_variaveis(texto))

#         form = FormularioDinamico(variaveis=variaveis)

#         return render(request, 'produzir_laudo.html', {'form': form, 'laudo': laudo})

#     def encontrar_variaveis(self, texto):
#         import re
#         # Usar expressão regular para encontrar as variáveis
#         return re.findall(r'<<(\w+)>>', texto)

    