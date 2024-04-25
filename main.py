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

saldo = 0
movimentacoes = []
qtde_saques = 0
limite_saque = 5000

lista_clientes = []
lista_contas = []
conta_seq = 1


def criar_conta(contas, clientes, sequencial):
    print("Criando uma nova conta corrente...")

    conta = dict()
    conta['agencia'] = '0001'
    conta['numero'] = sequencial

    cpf_cliente = input("Digite o CPF do cliente: ")
    cpf_cliente = cpf_cliente.replace(".", "").replace("-", "")
    cliente = buscar_cliente(clientes, cpf_cliente)
    if not cliente:
        print(f'Cliente com cpf: {cpf_cliente} não encontrado!')
        return

    conta['cliente'] = cliente

    print(f"Conta {sequencial} criada com sucesso!")
    contas.append(conta)


def buscar_cliente(clientes, cpf_cliente):
    for cliente in clientes:
        if cpf_cliente == cliente['cpf']:
            return cliente

    return None


def listar_contas(contas):
    if len(contas) > 0:
        for conta in contas:
            print(
                f"Agencia: {conta['agencia']} - Número: {conta['numero']} - Cliente: {conta['cliente']['nome']}"
            )
    else:
        print("Não há contas cadastradas!")


def criar_cliente(clientes):
    cliente = dict()
    cliente['nome'] = input("Digite o nome do cliente: ")

    cpf = input("Digite o CPF do cliente: ")
    cpf = cpf.replace(".", "").replace("-", "")
    cliente['cpf'] = cpf
    for cliente_existente in clientes:
        if cliente['cpf'] == cliente_existente['cpf']:
            print("Cliente já cadastrado anteriormente! ")
            return

    cliente['data_de_nascimento'] = input(
        "Digite a data de nascimento do cliente: ")

    logradouro = input("Digite a rua do cliente: ")
    numero = input("Digite o número da casa do cliente: ")
    cidade = input("Digite a cidade do cliente: ")
    uf = input("Digite a UF do cliente: ")

    cliente['endereco'] = f"{logradouro}, {numero}, {cidade}/{uf}"

    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")


def listar_clientes(clientes):
    if len(clientes) > 0:
        for cliente in clientes:
            print(f"Nome: {cliente['nome']} - CPF: {cliente['cpf']}")
    else:
        print("Não há clientes cadastrados!")


def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    saldo -= valor
    extrato.append(f"Saque: R${valor:.2f}")
    return saldo, extrato


def deposito(saldo, valor, extrato):
    saldo += valor
    print("Depósito realizado com sucesso!")
    extrato.append(f"Depósito: R${valor:.2f}")
    return saldo, extrato


def extrato(saldo, *, extrato):
    print("Extrato:")
    if len(extrato) > 0:
        for movimentacao in extrato:
            print(movimentacao)
    else:
        print("Nenhuma transação realizada.")
    print(f"Saldo: R${saldo:.2f}")


while True:
    opcao = int(input(menu))

    if opcao == 1:
        valor_deposito = float(input("Digite o valor do depósito: "))
        if valor_deposito > 0:
            saldo, movimentacoes = deposito(saldo, valor_deposito,
                                            movimentacoes)
        else:
            print("Valor inválido. Deve ser maior que zero.")
    elif opcao == 2:
        valor_saque = float(input("Digite o valor do saque: "))

        if valor_saque <= 0:
            print("O valor do saque deve ser positivo.")
            continue

        if valor_saque > 500:
            print("O valor do saque deve ser menor ou igual a R$500,00.")
            continue

        if qtde_saques >= 3:
            print("Você atingiu o limite de saques diários.")
            continue

        if valor_saque > saldo:
            print(
                "O valor do saque deve ser menor ou igual ao saldo disponível."
                f"Saldo disponível: R${saldo:.2f}")
            continue

        saldo, movimentacoes = saque(saldo=saldo,
                                     valor=valor_saque,
                                     extrato=movimentacoes,
                                     limite=500,
                                     numero_saques=qtde_saques,
                                     limite_saques=3)
        qtde_saques += 1

    elif opcao == 3:
        extrato(saldo, extrato=movimentacoes)
        continue

    elif opcao == 4:
        criar_cliente(lista_clientes)
        continue

    elif opcao == 5:
        listar_clientes(lista_clientes)
        continue

    elif opcao == 6:
        criar_conta(lista_contas, lista_clientes, conta_seq)
        conta_seq += 1
        continue
    elif opcao == 7:
        listar_contas(lista_contas)
        continue

    elif opcao == 8:
        print('Agradecemos a preferência. Até a próxima!')
        break

    else:
        print('Opção inválida. Tente novamente.')
        continue
