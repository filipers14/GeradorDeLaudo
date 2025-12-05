from django import forms
import pdb
from a_core.models import LaudoModelo, RedacaoModelo, TopicoModelo, VariaveisModelo

class FormRedacao(forms.ModelForm):
    class Meta:
        model = RedacaoModelo
        fields = ['nome_redacao', 'texto_redacao', 'setor_redacao']

class FormTopico(forms.ModelForm):
    class Meta:
        model = TopicoModelo
        fields = ['nome_topico', 'topico_pai', 'redacoes_associadas']

class FormLaudo(forms.ModelForm):
    class Meta:
        model = LaudoModelo
        fields = ['nome_laudo_modelo', 'topicos_associados','redacoes_associadas']

class FormVariavel(forms.ModelForm):
    class Meta:
        model = VariaveisModelo
        fields = ['nome_variavel','status']

class FormularioDinamico(forms.Form):
    def __init__(self, *args, **kwargs):
        variaveis = kwargs.pop('variaveis', [])
        super().__init__(*args, **kwargs)
        from a_core.models import ValorVariavelModelo, VariaveisModelo

        for variavel_obj in variaveis:
            var_nome = variavel_obj.nome_variavel  # Use o nome da variável como o nome do campo
            valores = ValorVariavelModelo.objects.filter(variavel_associada=variavel_obj, status='ativo')
            

            if valores.exists():
                escolhas = [(v.valor_variavel, v.valor_variavel) for v in valores]
                self.fields[var_nome] = forms.ChoiceField(label=var_nome, choices=escolhas, required=True)
            else:
                self.fields[var_nome] = forms.CharField(label=var_nome, required=True)
