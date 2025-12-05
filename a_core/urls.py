from django.urls import path

from .views import *

app_name = 'a_core'

urlpatterns = [
    path('', Home.as_view(), name='home'),

    path('redacao/', ListaRedacaoModelo.as_view(), name='lista_redacao_modelo'),
    path('laudo/', ListaLaudoModelo.as_view(), name='lista_laudo_modelo'),
    path('topico/', ListaTopicoModelo.as_view(), name='lista_topico_modelo'),

    path('redacao/criar/', CriarRedacaoModelo.as_view(), name='criar_redacao_modelo'),
    path('laudo/criar/', CriarLaudoModelo.as_view(), name='criar_laudo_modelo'),
    path('topico/criar/', CriarTopicoModelo.as_view(), name='criar_topico_modelo'),
    # path('valorvariavel/', CriarValorVariavel.as_view(), name='criar_valor_variavel'),

    path('redacao/editar/<int:pk>/', EditarRedacaoModelo.as_view(), name='editar_redacao_modelo'),
    path('laudo/editar/<int:pk>/', EditarLaudoModelo.as_view(), name='editar_laudo_modelo'),
    path('topico/editar/<int:pk>/', EditarTopicoModelo.as_view(), name='editar_topico_modelo'),

    path('redacao/<int:pk>/', DetalhesRedacaoModelo.as_view(), name='detalhes_redacao_modelo'),
    path('laudo/<int:pk>/', DetalhesLaudoModelo.as_view(), name='detalhes_laudo_modelo'),
    path('topico/<int:pk>/', DetalhesTopicoModelo.as_view(), name='detalhes_topico_modelo'),
    path('variavel/<int:pk>/', EditarVariavelModelo.as_view(), name='detalhes_variavel_modelo'),

    path('produzirlaudo/<int:pk>', ProduzirLaudo.as_view(), name='produzir_laudo'),

    path('deletarlaudomodelo/<int:pk>', DeletarLaudoModelo.as_view(), name='deletar_laudo_modelo'),

]