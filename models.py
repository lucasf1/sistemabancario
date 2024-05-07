from abc import ABC, abstractmethod


class Cliente:

    def __init__(self, endereco) -> None:
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        pass

    def adicionar_conta(self, conta):
        pass


class PessoaFisica(Cliente):

    def __init__(self, endereco, cpf, nome, data_nascimento) -> None:
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento


class Historico:

    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        pass


class Transacao(ABC):

    @classmethod
    @abstractmethod
    def registrar(cls, conta):
        pass


class Deposito(Transacao):

    def __init__(self, valor) -> None:
        super().__init__()
        self._valor = valor


class Saque(Transacao):

    def __init__(self, valor) -> None:
        super().__init__()
        self._valor = valor


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

    def sacar(self, valor: float):
        pass

    def depositar(self, valor: float):
        pass


class ContaCorrente(Conta):

    def __init__(self, numero, cliente, limite=500, limite_saques=3) -> None:
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saques
