from datetime import datetime

from models import ContaCorrente, ContaIterador, Deposito, PessoaFisica, Saque


def log_transacao(func):

    def envelope(*args, **kwargs):
        result = func(*args, **kwargs)
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(f"""
[{data_hora}] Função '{func.__name__}' executada com argumentos
{args} e {kwargs}. Resultado: {result}\n""")
        except IOError as ex:
            print(f"Erro ao acessar o arquivo: {ex}")

        print(f"{datetime.now()}: {func.__name__.upper()}")
        return result

    return envelope


def buscar_cliente(lista_clientes, cpf_cliente):

    for cliente in lista_clientes:
        if cpf_cliente == cliente.cpf:
            return cliente

    return None


def listar_clientes(lista_clientes):

    print()
    if len(lista_clientes) > 0:
        for cliente in lista_clientes:
            print(f"Nome: {cliente.nome} - CPF: {cliente.cpf}")
    else:
        print("\nERRO: Não há clientes cadastrados!")


@log_transacao
def criar_cliente(lista_clientes):

    cpf_cliente = input("Digite o CPF do cliente (somente números): ")
    cliente_bd = buscar_cliente(lista_clientes, cpf_cliente)
    if cliente_bd:
        print("\nERRO: Cliente já cadastrado anteriormente! ")
        return

    nome_cliente = input("Digite o nome do cliente: ")
    data_nasc_cliente = input("Digite a data de nascimento do cliente: ")

    logradouro_cliente = input("Digite a rua do cliente: ")
    numero_logr_cliente = input("Digite o número da casa do cliente: ")
    cidade_cliente = input("Digite a cidade do cliente: ")
    uf_cliente = input("Digite a UF do cliente: ")

    endereco_cliente = f"{logradouro_cliente}, {numero_logr_cliente}, {cidade_cliente}/{uf_cliente}"

    cliente = PessoaFisica(nome=nome_cliente,
                           data_nascimento=data_nasc_cliente,
                           cpf=cpf_cliente,
                           endereco=endereco_cliente)

    lista_clientes.append(cliente)
    print(f"\nCliente {cliente.nome} cadastrado com sucesso!")


def listar_contas(cliente):

    print()
    if cliente.contas:
        for conta in ContaIterador(cliente.contas):
            print(conta)
        return cliente.contas
    else:
        print("\nERRO: Não há contas cadastradas!")
        return None


@log_transacao
def criar_conta(lista_contas, lista_clientes, sequencial):

    print("\nCriando uma nova conta corrente...")

    cpf_cliente = input("Digite o CPF do cliente (somente números): ")
    cliente_bd = buscar_cliente(lista_clientes, cpf_cliente)
    if not cliente_bd:
        print("\nERRO: Cliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente_bd, numero=sequencial)

    print(f"\nConta {conta.numero} criada com sucesso!")
    lista_contas.append(conta)
    cliente_bd.contas.append(conta)


def recuperar_conta(cliente):

    print(f'Contas do cliente {cliente.nome}:')
    contas = listar_contas(cliente)

    if contas:
        conta_selecionada = int(input("Digite o número da conta desejada: "))
        for conta in contas:
            if conta.numero == conta_selecionada:
                return conta

        return None


def extrato(conta):
    print("Extrato:")

    extrato = ""
    if conta.historico.transacoes:
        for transacao in conta.historico.gerar_relatorio():
            extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    else:
        print("\nERRO: Nenhuma transação realizada.")

    print(extrato)
    print(f"Saldo: R${conta.saldo:.2f}")


@log_transacao
def depositar(lista_clientes):
    cpf_cliente = input("Digite o CPF do cliente (somente números): ")
    cliente_bd = buscar_cliente(lista_clientes, cpf_cliente)

    if not cliente_bd:
        print("\nERRO: Cliente não encontrado!")
    else:
        valor_deposito = float(input("Digite o valor do depósito: "))

        conta_selecionada = recuperar_conta(cliente_bd)
        if conta_selecionada:
            transacao = Deposito(valor_deposito)
            cliente_bd.realizar_transacao(conta_selecionada, transacao)
        else:
            print("Conta não encontrada!")


@log_transacao
def sacar(lista_clientes):
    cpf_cliente = input("Digite o CPF do cliente (somente números): ")
    cliente_bd = buscar_cliente(lista_clientes, cpf_cliente)

    if not cliente_bd:
        print("\nERRO: Cliente não encontrado!")
    else:
        valor_saque = float(input("Digite o valor do saque: "))

        conta_selecionada = recuperar_conta(cliente_bd)
        if conta_selecionada:
            transacao = Saque(valor_saque)
            cliente_bd.realizar_transacao(conta_selecionada, transacao)
        else:
            print("Conta não encontrada!")


@log_transacao
def exibir_extrato(lista_clientes):
    cpf_cliente = input("Digite o CPF do cliente (somente números): ")
    cliente_bd = buscar_cliente(lista_clientes, cpf_cliente)

    if not cliente_bd:
        print("\nERRO: Cliente não encontrado!")
    else:
        conta_selecionada = recuperar_conta(cliente_bd)
        if conta_selecionada:
            extrato(conta=conta_selecionada)
        else:
            print("Conta não encontrada!")


def main():

    lista_clientes = []
    lista_contas = []
    conta_seq = 1

    def mostrar_menu():
        menu = """
            Digite o número da opção desejada:

            1 - Para Depositar
            2 - Para Sacar
            3 - Para Extrato    
            4 - Para criar um novo cliente
            5 - Para listar os clientes
            6 - Para criar uma conta corrente
            7 - Para listar as contas corrente
            8 - Para Sair

        """

        print(menu)

    while True:
        mostrar_menu()
        opcao = int(input("Opção desejada:"))

        if opcao == 1:  # Depositar
            depositar(lista_clientes)

        elif opcao == 2:  # Sacar
            sacar(lista_clientes)

        elif opcao == 3:  # Extrato
            exibir_extrato(lista_clientes)

        elif opcao == 4:  # Criar um novo cliente
            criar_cliente(lista_clientes)

        elif opcao == 5:  # Listar os clientes
            listar_clientes(lista_clientes)

        elif opcao == 6:  # Criar uma conta corrente

            criar_conta(lista_contas, lista_clientes, conta_seq)
            conta_seq += 1

        elif opcao == 7:  # Listar as contas corrente de um cliente

            cpf_cliente = input("Digite o CPF do cliente (somente números): ")
            cliente_bd = buscar_cliente(lista_clientes, cpf_cliente)

            if not cliente_bd:
                print("\nERRO: Cliente não encontrado!")
            else:
                listar_contas(cliente_bd)

        elif opcao == 8:  # Sair
            print('Agradecemos a preferência. Até a próxima!')
            break

        else:  # Opção inválida
            print('\nERRO: Opção inválida. Tente novamente.')


if __name__ == "__main__":
    main()
