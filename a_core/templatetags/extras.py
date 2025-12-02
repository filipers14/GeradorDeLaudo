# a_core/templatetags/extras.py

# Importa o módulo "template" do Django, necessário para criar filtros customizados para templates
from django import template

# Cria um objeto de registro de biblioteca de filtros, necessário para registrar novos filtros
register = template.Library()

# Registra a função abaixo como um filtro customizado no Django template system
@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor associado à chave 'key' no dicionário passado como parâmetro.
    Útil para acessar dinamicamente valores de dicionários dentro dos templates Django.
    """
    # Usa o método get do dicionário para tentar obter o valor da chave.
    # Se a chave não existir, retorna None por padrão.
    return dictionary.get(key)
