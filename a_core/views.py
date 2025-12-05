from typing import Any
import pdb

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
    # Define o modelo que será utilizado para update: VariaveisModelo
    model = VariaveisModelo
    
    # Define o template HTML que será usado para renderizar o formulário de edição
    template_name = 'form.html'
    
    # Define qual formulário será utilizado para representar o modelo
    form_class = FormVariavel

    def get_context_data(self, **kwargs):
        # Obtém o contexto padrão do método da superclasse e adiciona informações extras
        context = super().get_context_data(**kwargs)
        
        # Declaração do formset dinâmico atrelado à variável para os valores da variável;
        # Usa inlineformset_factory para ligar VariaveisModelo <-> ValorVariavelModelo via ForeignKey,
        # incluindo os campos 'valor_variavel' e 'status', permitindo um extra (mínimo 1) e remoção (can_delete=True)
        ValorVariavelFormSet = inlineformset_factory(
            VariaveisModelo,              # Modelo principal
            ValorVariavelModelo,          # Modelo do formset inline
            fields=('valor_variavel', 'status'),  # Campos do formset
            extra=1,                      # Sempre um formulário extra (vazio) para adicionar novo valor
            can_delete=True               # Permite excluir valores existentes
        )
        
        # Se a requisição for POST, inicializa o formset com os dados enviados pelo usuário
        if self.request.method == 'POST':
            # Cria o formset com os dados POSTando e instancia vinculada ao objeto editado
            formset = ValorVariavelFormSet(self.request.POST, instance=self.object)
        else:
            # Caso contrário, inicializa o formset apenas com o objeto atual para exibir valores existentes
            formset = ValorVariavelFormSet(instance=self.object)
        
        # Adiciona o formset ao contexto para acesso no template e processamento posterior
        context['formset'] = formset
        # Retorna o contexto enriquecido para ser usado na renderização do template
        return context

    def form_valid(self, form):
        # Recupera o contexto (com formset incluso) – faz nova chamada para garantir consistência em casos edge-case
        context = self.get_context_data()
        # Obtém o formset do contexto para processar submissão múltipla (form principal + inline)
        formset = context['formset']
        # Verifica se o formset é válido (campos filhos)
        if formset.is_valid():
            # Salva o formulário principal (atualiza a variável)
            self.object = form.save()
            # Vincula o formset (modelo filho) ao objeto salvo/atualizado
            formset.instance = self.object
            # Salva todos os objetos filhos submetidos pelo formset, incluindo alterações e novas criações
            formset.save()
            # Recupera a chave primária do laudo associado para redirecionamento pós-salvamento
            laudo_pk = self.object.laudo_associado.pk
            # Redireciona o usuário para a página de detalhes do laudo associado, indicando sucesso
            return redirect('a_core:detalhes_laudo_modelo', pk=laudo_pk)
        else:
            # Caso qualquer formulário filho seja inválido, retorna resposta de formulário inválido
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        # Ao receber um POST, define o objeto que será editado
        self.object = self.get_object()
        # Obtém o formulário principal já preenchido com os dados do POST
        form = self.get_form()
        # Recupera o contexto (incluindo o formset carregado com request.POST)
        context = self.get_context_data(**kwargs)
        # Obtém o formset do contexto para validação
        formset = context['formset']
        # Verifica se tanto o formulário principal quanto o formset são válidos
        if form.is_valid() and formset.is_valid():
            # Se ambos estiverem válidos, chama o método padrão para salvar tudo adequadamente
            return self.form_valid(form)
        else:
            # Se houver qualquer erro em algum dos formulários ou formsets, exibe novamente o formulário para correção
            return self.form_invalid(form)

    def get_success_url(self):
        # Ao concluir a operação com sucesso, determina dinamicamente a URL para redirecionamento,
        # utilizando a chave primária do laudo associado ao objeto editado
        laudo_pk = self.object.laudo_associado.pk
        # Retorna a URL reversa para a view de detalhes do laudo modelo correspondente
        return reverse_lazy('a_core:detalhes_laudo_modelo', kwargs={'pk': laudo_pk})

class ProduzirLaudo(View):
    def get(self, request, pk):
        laudo = get_object_or_404(LaudoModelo, pk=pk)

        variaveis_laudo = laudo.variaveismodelo_set.filter(status='ativo')

        form = FormularioDinamico(variaveis = variaveis_laudo)

        return render(request, 'produzir_laudo.html', {'form':form, 'laudo':laudo})
    pass


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

    