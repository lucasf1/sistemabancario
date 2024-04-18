menu = """
    Digite o número da opção desejada:
    
    1 - Para Depositar
    2 - Para Sacar
    3 - Para Extrato
    4 - Para Sair
"""

saldo = 0
movimentacoes = []

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
        pass
    elif opcao == 3:
        pass
    elif opcao == 4:
        print('Agradecemos a preferência. Até a próxima!')
        break
    else:
        print('Opção inválida. Tente novamente.')
        continue
