from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:

    def __init__(self, endereco) -> None:

        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("ERRO: Limite de transações diárias atingido!")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas


class PessoaFisica(Cliente):

    def __init__(self, endereco, cpf, nome, data_nascimento) -> None:

        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ({self.cpf})>"

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf


class Historico:

    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):

        self._transacoes.append({
            "tipo":
            transacao.__class__.__name__,
            "valor":
            transacao.valor,
            "data":
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower(
            ) == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"],
                                               "%d-%m-%Y %H:%M:%S").date()
            if data_transacao == data_atual:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):

    def __init__(self, valor) -> None:

        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):

    def __init__(self, valor):

        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class ContaIterador:

    def __init__(self, contas):
        self._contas = contas
        self._contador = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self._contas[self._contador]
            return conta
        except IndexError:
            raise StopIteration
        finally:
            self._contador += 1


class Conta:

    def __init__(self, numero, cliente) -> None:

        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):

        if valor > self._saldo:
            print(
                f"\nERRO: O valor do saque deve ser menor ou igual ao saldo disponível. Saldo disponível: R${self._saldo:.2f}"
            )
        elif valor <= 0:
            print("\nERRO: O valor do saque deve ser positivo.")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True

        return False

    def depositar(self, valor):

        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
            return True
        else:
            print("\nERRO: Valor inválido. Deve ser maior que zero.")
            return False


class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3) -> None:

        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saques

    def sacar(self, valor):

        # conta o número de saques diários
        numero_saques = len([
            transacao for transacao in self.historico.transacoes
            if transacao["tipo"] == Saque.__name__
        ])

        if numero_saques >= self._limite_saque:
            print("\nERRO: Você atingiu o limite de saques diários.")
        elif valor > self._limite:
            print(
                f"\nERRO: O valor do saque deve ser menor ou igual a {self._limite:.2f}."
            )

        else:
            return super().sacar(valor)

        return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
