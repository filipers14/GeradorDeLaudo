from django import forms

from a_core.models import LaudoModelo, RedacaoModelo, TopicoModelo

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