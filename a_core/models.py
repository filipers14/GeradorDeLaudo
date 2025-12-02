from django.contrib.admin.utils import help_text_for_field
from django.db import models


# Create your models here.
class RedacaoModelo(models.Model):
    '''
    Redação modelo refere-se a um texto com variáveis devidamente padronizadas para ser utilizada em um tópico/laudo posteriormente.
    '''
    nome_redacao = models.CharField(max_length = 150, verbose_name = 'Nome da Redação', help_text  = "Insira o nome da redação")
    texto_redacao = models.TextField(verbose_name = 'Texto da Redação', help_text ='Insidera o texto modelo da redação, colocando as variáveis no padrão <<NOME_VARIAVEL>>.' )
    setor_redacao = models.ForeignKey('Setor', on_delete=models.CASCADE, verbose_name = 'Setor', help_text = 'Setor associado à redação.', blank = True, null = True)
    

    STATUS_CHOICES = (('ativo', 'Ativo'), ('inativo', 'Inativo'),)

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        return self.nome_redacao


class VariaveisModelo(models.Model):
    '''
    Uma variável modelo é uma variável
    '''
    nome_variavel = models.CharField(max_length=150, verbose_name = 'Nome da Variável')
    string_substituicao = models.CharField(max_length=150, verbose_name = 'String de Substituição')
    TIPO_CAMPO =[
        ('Campo Aberto', "Campo Aberto"),
        ('Campo Seletor', 'Campo Seletor'),
    ]
    tipo_campo = models.CharField(choices=TIPO_CAMPO, verbose_name = 'Tipo de Variável')

    STATUS_CHOICES = (('ativo', 'Ativo'), ('inativo', 'Inativo'),)

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')

    def __str__(self):
        return self.nome_variavel

class ValorVariavelModelo(models.Model):
    variavel_associada = models.ForeignKey(VariaveisModelo, on_delete= models.CASCADE, verbose_name = 'Variável Associada')
    valor_variavel = models.CharField(verbose_name = 'Valor da Variável')

    STATUS_CHOICES = (('ativo', 'Ativo'), ('inativo', 'Inativo'),)

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')

    def __str__(self):
        return self.valor_variavel

class TopicoModelo(models.Model):
    nome_topico = models.CharField(max_length=150, verbose_name="Nome do Tópico")
    topico_pai = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    redacoes_associadas = models.ManyToManyField(
        'RedacaoModelo', 
        through='TopicoRedacao',
        verbose_name="Redações Associadas"
    )

    STATUS_CHOICES = (('ativo', 'Ativo'), ('inativo', 'Inativo'),)

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')

    def __str__(self):
        return self.nome_topico

class TopicoRedacao(models.Model):
    topico = models.ForeignKey('TopicoModelo', on_delete=models.CASCADE)
    redacao = models.ForeignKey('RedacaoModelo', on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem da Redação no Tópico")

    class Meta:
        unique_together = ('topico', 'redacao')
        ordering = ['ordem']

    def __str__(self):
        return f'{self.topico} - {self.redacao} (Ordem: {self.ordem})'

class LaudoModelo(models.Model):
    nome_laudo_modelo = models.CharField(max_length=150, verbose_name='Nome do Laudo')
    topicos_associados = models.ManyToManyField(
        'TopicoModelo',
        through='LaudoTopico',
        verbose_name="Tópicos Associados"
    )
    redacoes_associadas = models.ManyToManyField(
        'RedacaoModelo',
        through='LaudoRedacao',
        verbose_name="Redações Associadas",
        blank = True,
        null = True
    )

    def __str__(self):
        return self.nome_laudo_modelo

class LaudoTopico(models.Model):
    laudo = models.ForeignKey('LaudoModelo', on_delete=models.CASCADE)
    topico = models.ForeignKey('TopicoModelo', on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem do Tópico")

    class Meta:
        unique_together = ('laudo', 'topico')
        ordering = ['ordem']

    def __str__(self):
        return f'{self.laudo} - {self.topico} (Ordem: {self.ordem})'

class LaudoRedacao(models.Model):
    laudo = models.ForeignKey('LaudoModelo', on_delete=models.CASCADE)
    redacao = models.ForeignKey('RedacaoModelo', on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=0, verbose_name="Ordem da Redação")

    class Meta:
        unique_together = ('laudo', 'redacao')
        ordering = ['ordem']

    def __str__(self):
        return f'{self.laudo} - {self.redacao} (Ordem: {self.ordem})'


class Setor(models.Model):
    nome_setor = models.CharField(max_length=100, verbose_name="Nome do Setor")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição do Setor")

    STATUS_CHOICES = (('ativo', 'Ativo'), ('inativo', 'Inativo'),)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def __str__(self):
        return self.nome_setor

