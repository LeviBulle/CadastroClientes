clientes = []

while True:
    print('-=' * 20)
    print('[1]CADASTAR CLIENTE')
    print('[2]VERIFICAR CLIENTES CADASTRADOS')
    print('[3]BUSCAR UM CLIENTE')
    print('[4]EXCLUIR CADASTRO')
    print('[0]SAIR')
    menu = int(input('SELECIONE A OPÇÃO QUE DESEJA ACESSAR: '))

    if menu == 1:
        while True:
            print('-=' * 20)
            cadastro = str(input('Deseja cadastrar um cliente [S/N]? ').upper().strip())
            if cadastro not in 'SN':
                print('OPÇÃO INVÁLIDA!')
            elif cadastro == 'S':
                cliente = []
                cliente.append(str(input('NOME: ').upper().strip()))
                cliente.append(input('TELEFONE: ').strip())
                cliente.append(str(input('E-MAIL: ').upper().strip()))
                clientes.append(cliente)
            elif cadastro == 'N':
                break



    elif menu == 2:
        while True:
            print('-=' * 20)
            listar_clientes = str(input('Deseja verificar todos os clientes cadastrados [S/N]? ').strip().upper())
            if listar_clientes not in 'SN':
                print('OPÇÃO INVÁLIDA!')
            elif listar_clientes == 'S':
                if len(clientes) == 0:
                    print('Nenhum cliente cadastrado.')
                else:
                    for c in clientes:
                        print(f'Nome: {c[0]}')
                        print(f'Telefone: {c[1]}')
                        print(f'E-mail: {c[2]}')
                        print('-' * 30)
            elif listar_clientes == 'N':
                break


    elif menu == 3:
        while True:
            print('-=' * 20)
            buscar = str(input('Deseja buscar um cliente [S/N]?').strip().upper())
            if buscar not in 'SN':
                print('OPÇÃO INVÁLIDA!')
            elif buscar == 'S':
                nome = str(input('Informe o nome do cliente que deseja buscar: ').upper().strip())
                encontrado = False
                for busca in clientes:
                    if nome == busca[0]:
                        encontrado = True
                        print('-=' * 20)
                        print(f'CLIENTE {busca[0]} ENCONTRADO.')
                        while True:
                            print('-=' * 20)
                            print('[1]TELEFONE')
                            print('[2]E-MAIL')
                            print('[0]SAIR')
                            opcao = str(input('SELECIONE UMA OPÇÃO: ').upper().strip())
                            if opcao == '1':
                                print(f'>>>> TELEFONE: {busca[1]}')
                            elif opcao == '2':
                                print(f'>>>> E-MAIL: {busca[2]}')
                            elif opcao == '0':
                                break
                        break
                if not encontrado:
                     print(f'Cliente {nome} não encontrado! Tente novamente!')
            elif buscar == 'N':
                break


    elif menu == 4:
        while True:
            print('-=' * 20)
            excluir = str(input('Deseja excluir um cadastro? [S/N]').strip().upper())
            if excluir not in 'SN':
                print('OPÇÃO INVÁLIDA!')
            elif excluir == 'S':
                nome = str(input('Informe o nome do cliente que deseja deletar o cadastro: ').upper().strip())
                excluido = False
                for ex in clientes:
                    if nome == ex[0]:
                        excluido = True
                        clientes.remove(ex)
                        print(f'CLIENTE {ex[0]} EXCLUIDO COM SUCESSO.')
                        break
                if not excluido:
                     print(f'Cliente {nome} não encontrado! Tente novamente!')
            elif excluir == 'N':
                break

    elif menu == 0:
        break
