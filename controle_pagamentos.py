import hashlib
import csv
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SENHA_HASH = hashlib.sha256("suasenha".encode()).hexdigest() # senha criptografada, a senha deve ser salva no banco

Base= declarative_base()
datas= date.today()

class Cliente(Base):
    __tablename__ = "clientes"
    id= Column(Integer, primary_key=True)
    data= Column(String)
    nomes= Column(String)
    cpfs= Column(Integer)
    valores= Column(Integer)
    tipos= Column(String)
    contatos= Column(Integer)
    enderecos= Column(String)

# armazenando os pagamentos
pagamentos= []

# verificar senha
def verificar_senha():
    senha= input("Digite senha para acesso: ")
    if hashlib.sha256(senha.encode()).hexdigest() == SENHA_HASH:
        print("\nAcesso liberado!\n")
        return True
    else:
        print("\nSenha incorreta.\n")
        return False

# cadastrando pagamentos
def cadastro_pagamento():
    try:
        nome= input("Nome do cliente: ")
        cpf= int(input("Informe CPF: "))
        valor= float(input("Valor do pagamento (R$): "))
        if valor <= 0:
            print("\nErro: valor deve ser maior que 0.\n")
            return
        tipo= input("Forma de pagamento (Dinheiro, Pix, Cartao): ")
        contato= int(input("Telefone pra contato: "))
        endereco= input("Informe endereço: ")
    except ValueError:
        print("\nErro: valor invalido.\n")
        return
    pagamentos.append({
        "cliente": nome,
        "cpf": cpf,
        "valor": valor,
        "metodo": tipo,
        "contato": contato,
        "endereco": endereco,
    })
    engine = create_engine("sqlite:///pagamentos.db")
    Base.metadata.create_all(engine)
    Session= sessionmaker(bind= engine)
    session= Session()
    # os dados sensiveis estaram disponiveis somente no banco
    novo_cliente= Cliente(data=datas, nomes= nome, cpfs= cpf, valores= valor, tipos= tipo, contatos= contato, enderecos= endereco)
    session.add(novo_cliente)
    session.commit()
    print("\nPagamento cadastrado com sucesso!\n")

# listando pagamentos
def listar_pagamentos():
    if not pagamentos:
        print("\nNenhum pagamento registrado.\n")
        return
    print("\nLista de pagamentos:\n")
    for i, pagui in enumerate(pagamentos, 1):
        print(f"{i}. Cliente: {pag['cliente']} | Cpf: {pag['cpf']} | Valor: R${pag['valor']:.2f} | Método: {pag['metodo']} | Contato: {pag['contato']} | Endereço: {pag['endereco']}")

#salva pagamentos em arquivo .CSV
def salvar_csv():
    if not pagamentos:
        print("\nNenhum pagamento para salvar.\n")
        return
    with open("pagamentos.csv", "w", newline="", encoding="utf-8") as arquivo:
        entrada_dados= ["cliente", "cpf", "valor", "metodo", "contato", "endereco"]
        escreva= csv.DictWriter(arquivo, fieldnames= entrada_dados)
        escreva.writeheader()
        escreva.writerows(pagamentos)
    print("\nPagamentos salvos no arquivo 'pagamentos.csv'!\n")

# gerar relatorio de total
def gerar_relatorio():
    if not pagamentos:
        print("\nNenhum pagamento registrado.\n")
        return
    total= sum(pag['valor'] for pag in pagamentos)
    print(f"\nTotal recebido: R${total:.2f}\n")

# Menu
def menu():
    while True:
        print("""
***** Menu de Pagamentos ******
    1. Cadastrar novo pagamento
    2. Listar pagamentos
    3. Salvar pagamentos em arquivo CSV
    4. Gerar relatorio de total
    5. Sair
""")
        opcao= input("Selecione uma opçao: ")
        if opcao == "1":
            cadastro_pagamento()
        elif opcao == "2":
            listar_pagamentos()
        elif opcao == "3":
            salvar_csv()
        elif opcao == "4":
            gerar_relatorio()
        elif opcao == "5":
            print("\nSaindo do sistema...\n")
            break
        else:
            print("\nOpçao invalida.\n")

if __name__ == "__main__":
    if verificar_senha():
        menu()

