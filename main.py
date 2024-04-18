menu = """
    Digite o número da opção desejada:
    
    1 - Para Depositar
    2 - Para Sacar
    3 - Para Extrato
    4 - Para Sair
"""

saldo = 0
movimentacoes = []
qtde_saques = 0
limite_saque = 5000

while True:
    opcao = int(input(menu))

    if opcao == 1:
        valor_deposito = float(input("Digite o valor do depósito: "))
        if valor_deposito > 0:
            saldo += valor_deposito
            print("Depósito realizado com sucesso!")
            movimentacoes.append(f"Depósito: R${valor_deposito:.2f}")
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

        saldo -= valor_saque
        qtde_saques += 1
        movimentacoes.append(f"Saque: R${valor_saque:.2f}")

    elif opcao == 3:
        print("Extrato:")
        if len(movimentacoes) > 0:
            for movimentacao in movimentacoes:
                print(movimentacao)
        else:
            print("Nenhuma transação realizada.")
        print(f"Saldo: R${saldo:.2f}")
    elif opcao == 4:
        print('Agradecemos a preferência. Até a próxima!')
        break
    else:
        print('Opção inválida. Tente novamente.')
        continue
