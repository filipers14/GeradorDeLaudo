# a_core/templatetags/extras.py

# Para essa tag (filtro customizado) funcionar, siga estes passos:
# 1. Crie uma pasta chamada "templatetags" dentro do seu app (já existe neste caso: a_core/templatetags).
# 2. Garanta que exista um arquivo __init__.py dentro dessa pasta para que vire um pacote Python.
# 3. Defina o filtro customizado neste arquivo (conforme abaixo).
# 4. Nos seus templates, carregue o filtro com {% load extras %}, onde "extras" é o nome deste arquivo (sem .py).
# 5. Utilize o filtro normalmente no template, ex: {{ dict|get_item:somekey }}

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor associado à chave 'key' no dicionário passado como parâmetro.
    Útil para acessar dinamicamente valores de dicionários dentro dos templates Django.
    """
    return dictionary.get(key)
