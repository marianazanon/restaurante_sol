from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone

BRAZILIAN_STATES = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

class Cliente(models.Model):

    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1)
    idade = models.IntegerField()
    nascimento = models.DateField()
    pontos = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='check_gender',
                check=Q(sexo = 'm') | Q(sexo = 'f') | Q(sexo = 'o'),
                violation_error_message='Sexo inválido, escolha entre masculino, feminino ou outro.'
            )
        ]
    
    def __str__(self):
        return self.nome

    def adicionar_pontos(self, valor):
        pontos_adicionados = int(valor // 10)
        self.pontos += pontos_adicionados
        self.save()
        return pontos_adicionados    

class Prato(models.Model):
    
        nome = models.CharField(max_length=100)
        descricao = models.TextField()
        valor = models.DecimalField(max_digits=8, decimal_places=2)
        disponivel = models.BooleanField(default=True)
    
        def __str__(self):
            return self.nome
        
class Fornecedor(models.Model):
        
        nome = models.CharField(max_length=100)
        estado = models.CharField(max_length=2)

        class Meta:
            constraints = [
                models.CheckConstraint(
                    name='check_state',
                    check=Q(estado__in=BRAZILIAN_STATES),
                    violation_error_message='Estado inválido, escolha um estado brasileiro.'
                )
            ]
        
        def __str__(self):
            return self.nome

class Ingredientes(models.Model):
    
    nome = models.CharField(max_length=100)
    data_fabricacao = models.DateField()
    data_validade = models.DateField()
    quantidade = models.IntegerField()
    observacao = models.CharField(max_length=100)

    class meta:
        constraints = [
            models.CheckConstraint(
                name='check_validade_after_fabricacao',
                check=Q(data_validade__gt=models.F('data_fabricacao')),
                violation_error_message='Data de fabricação não pode ser maior que a data de validade.'
            )
        ]
    
    def __str__(self):
        return self.nome

class Usos(models.Model):
    
    prato = models.ForeignKey(Prato, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingredientes, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Uso de {self.ingrediente.nome} em {self.prato.nome}"

class EventLog_Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

class Reajuste(models.Model):
    pct_reajuste = models.DecimalField(max_digits=5, decimal_places=2)
    prato = models.CharField(max_length=100)

    def __str__(self):
        return f"Reajuste {self.pct_reajuste}% for {self.prato}"

class Sorteio(models.Model):
    pass

    def __str__(self):
        return "Sorteio"

class Venda(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    prato = models.ForeignKey(Prato, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    dia = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
        
@receiver(pre_save, sender=Venda)
def calculate_valor(sender, instance, **kwargs):
    instance.valor = instance.prato.valor * instance.quantidade
    pontos = instance.cliente.adicionar_pontos(instance.valor)
    print(f"Cliente {instance.cliente.nome} ganhou {pontos} pontos na compra de {instance.prato.nome}.")