import requests
import matplotlib.pyplot as plt
import numpy as np

url_jogos = "http://localhost:3000/jogos"
# url_jogos = "https://api-trabalho-final.vercel.app/jogos"
url_usuarios = "http://localhost:3000/usuarios"
# url_usuarios = "https://api-trabalho-final.vercel.app/usuarios"
url_login = "http://localhost:3000/login"
# url_login = "https://api-trabalho-final.vercel.app/login"


# --------------------------------------------- Função de Título
def titulo(texto, sublinhado="-"):
  
  print()
  print(texto)
  print(sublinhado*40)

# Função para pausar a execução do programa
def continuar():
  input("Pressione ENTER para continuar...")

# Função para realizar o login do usuário

def login():
  titulo("Login do Usuário")

  email = input("E-mail: ")
  senha = input("Senha: ")

  response = requests.post(url_login, 
                            json={"email": email, 
                                  "senha": senha}
                          )
    
  if response.status_code == 200:
    usuario = response.json()
    print(f"Bem Vinde {usuario['nome']}!")
    return usuario['token']  
    
  else:
    print('-'*18+"Erro"+'-'*18)
    print(response.json()['erro'])
    print('-'*40)


# Função para realizar o cadastro do usuário
def cadastro():
  titulo("Cadastro de Usuário")

  nome = input("Nome: ")
  email = input("E-mail: ")
  senha = input("Senha: ")

  response = requests.post(url_usuarios, 
                            json={"nome": nome, 
                                  "email": email, 
                                  "senha": senha}
                          )
    
  if response.status_code == 201:
    print("Ok! Usuário cadastrado com sucesso")
  else:
    print('-'*18+"Erro"+'-'*18)
    print(response.json()['erro'])
    print('-'*40)
    continuar()
# --------------------------------------------- Funções de CRUD
def incluir():
  titulo("Inclusão de Jogos")
  
  nome    = input("Título do Jogo: ")
  descricao  = input("Descrição.........: ") 
  genero  = input("Gênero.........: ") 
  preco   = float(input("Preço R$.......: "))

  response = requests.post(url_jogos, 
                           json={"nome": nome, 
                                 "descricao": descricao,
                                 "genero": genero, 
                                 "preco": preco
                                 },
                           headers={"authorization": token}
                          )
  
  if response.status_code == 201:
    jogo = response.json()
    print(f"Ok! Jogo cadastrado com o código: {jogo['id']}")
  else:
    print("Erro... Não foi possível realizar a inclusão")

def listar():
  titulo("Lista dos Jogos Cadastrados")

  print("Cód. Título do Jogo..............: Gênero.....:  Preço R$:")
  print("="*58)

  response = requests.get(url_jogos)

  if response.status_code != 200:
    print("Erro... Não foi possível obter dados da API")
    return
  
  jogos = response.json()
  jogos = sorted(jogos, key=lambda x: x['id'])

  for jogo in jogos:
    if jogo["preco"] == 0.1:
      print(f"{jogo['id']:4d} {jogo['nome']:30s} {jogo['genero']:13s} Gratuíto")
    else:
      print(f"{jogo['id']:4d} {jogo['nome']:30s} {jogo['genero']:12s} {jogo['preco']:9.2f}")



def alterar():
  listar()  
  
  titulo("Alteração do Preço dos Jogos")

  id = int(input("Código do Jogo: "))

  # obtém os dados da API (para verificar se existe e os dados)
  response = requests.get(url_jogos)  
  jogos = response.json()

  jogo = [x for x in jogos if x['id'] == id]

  if len(jogo) == 0:
    print("Erro... Código de Jogo Inválido")
    return

  print(f"Título do Jogo : {jogo[0]['nome']}")
  print(f"Gênero.........: {jogo[0]['genero']}") 
  print(f"Preço R$.......: {jogo[0]['preco']:9.2f}")
  print()
  print(url_jogos+"/"+str(id))

  novo_preco = float(input("Novo Preço R$: "))

  response = requests.put(url_jogos+"/"+str(id), 
                          json={"preco": novo_preco},
                          headers={"authorization": token})
  
  if response.status_code == 200:
    jogo = response.json()
    print("Ok! Preço do jogo alterado com sucesso")
  else:
    print("Erro... Não foi possível realizar a alteração")


def excluir():
  listar()  
  
  titulo("Exclusão de Jogos")

  id = int(input("Código do Jogo: "))

  # obtém os dados da API (para verificar se existe e os dados)
  response = requests.get(url_jogos)  
  jogos = response.json()

  jogo = [x for x in jogos if x['id'] == id]

  if len(jogo) == 0:
    print("Erro... Código de Jogo Inválido")
    return

  print(f"Título do Jogo:  {jogo[0]['nome']}")
  print(f"Gênero.........: {jogo[0]['genero']}") 
  print(f"Preço R$.......: {jogo[0]['preco']:9.2f}")
  print()

  confirma = input("Confirma a Exclusão deste Jogo(S/N)? ").upper()

  if confirma == "S":
    response = requests.delete(url_jogos+"/"+str(id),
                               headers={"authorization": token})
  
    if response.status_code == 200:
      print("Ok! Jogo Excluído com sucesso")
    else:
      print("Erro... Não foi possível excluir este jogo")


# --------------------------------------------- Funções de Busca
def preco():
  titulo("Busca por Faixa de Preço")

  preco_min = float(input("Preço Mínimo R$: "))
  preco_max = float(input("Preço Máximo R$: "))

  response = requests.get(url_jogos)
  jogos = response.json()

  print("="*58)
  print("Cód. Título do Jogo..............: Gênero.....:  Preço R$:")
  print("="*58)

  for jogo in jogos:
    if preco_min <= jogo['preco'] <= preco_max:
      print(f"{jogo['id']:4d} {jogo['nome']:30s} {jogo['genero']:12s} {jogo['preco']:9.2f}")
      

# --------------------------------------------- Gráfico de Gêneros usando Matplotlib e Numpy 

def grafico():
  titulo("Gráfico Relacionando Gêneros dos Jogos")

  response = requests.get(url_jogos)
  jogos = response.json()

  labels = list(set([x['genero'] for x in jogos]))
  sizes = [0] * len(labels)

  for jogo in jogos:
    indice = labels.index(jogo['genero'])
    sizes[indice] += 1

  fig, ax = plt.subplots()
  ax.pie(sizes, labels=labels, autopct='%1.1f%%')

  plt.show()


# --------------------------------------------- Funções de Descrição
def descricao():
  listar()  
  
  titulo("Descrição do Jogo")

  id = int(input("Digite o número do jogo a qual deseja visualizar sua descrição:  "))

  # obtém os dados da API (para verificar se existe e os dados)
  response = requests.get(url_jogos)  
  jogos = response.json()

  jogo = [x for x in jogos if x['id'] == id]

  if len(jogo) == 0:
    print("Erro... Código de Jogo Inválido")
    return

  print(f"Descrição de {jogo[0]['nome']}:")
  print("="*23)
  print(f"{jogo[0]['descricao']:12s}")
    

# --------------------------------------------- Função de segurança para alterar senha do usuário (já logado)

def AlterarSenha():
  titulo("Alterar Senha")
  print("Digite seu e-mail e senha para continuar")
  email = input("E-mail: ")
  senha = input("Senha: ")
  
  response = requests.post(url_login, 
                            json={"email": email, 
                                  "senha": senha}
                          )
  
  if response.status_code == 200:
    usuario = response.json()
    id = usuario['id']
    
    nova_senha = input("Digite sua nova senha: ")
    confirmar_senha = input("Confirme sua nova senha: ")
    
    if nova_senha == confirmar_senha:
      response = requests.put(url_usuarios+"/mudarsenha/"+str(id), 
                              json={"senhaAntiga": senha,
                                    "senhaNova": nova_senha},
                              headers={"authorization": token})
      if response.status_code == 200:
        print("Senha alterada com sucesso!")
        continuar()
      else:
        print(response.json()['erro'])
        continuar()
    else:
      print("Erro... As senhas não batem")
      continuar()
  else:
    print("Erro... Não foi possível alterar a senha")
    continuar()

# Loop para realizar o login ou cadastro do usuário
token = None

while token is None:
  titulo("Bem Vindo ao Cadastro de Jogos - Uso de API")
  print("1. Login")
  print("2. Cadastro")
  print("3. Sair")
  opcao = int(input("Opção: "))
  if opcao == 1:
    token = login()
    if token == None:
      print("Erro ao realizar o login, tente novamente ou entre em contato com o suporte.")
      continuar()
  elif opcao == 2:
    cadastro()
  else:
    print("="*16)
    print("Volte sempre! :)")
    exit()
    

# -------------------------------------------- Menu Principal inicial

def configuracoes():
  while True:
    titulo("Configurações de Conta")
    print("1. Alterar senha")
    print("0. Voltar")
    
    opcao = int(input("Opção: "))
    
    if opcao == 1:
      AlterarSenha()
      break
    else:
      print("="*16)
      print("Volte sempre! :)")
      break
    
    
# Loop Principal
while True:
  titulo("Cadastro de Jogos - Uso de API")
  print("1. Inclusão de Jogos")
  print("2. Listagem de Jogos")
  print("3. Alteração de preço Jogos")
  print("4. Exclusão de Jogos")
  print("5. Busca por faixa de preço")
  print("6. Gráfico Comparando Gêneros")
  print("7. Visualizar Descrição do jogo")
  print("8. Configurações de Conta")
  print("0. Finalizar")
  opcao = int(input("Opção: "))
  if opcao == 1:
    incluir()
  elif opcao == 2:
    listar()
  elif opcao == 3:
    alterar()
  elif opcao == 4:
    excluir()
  elif opcao == 5:
    preco()
  elif opcao == 6:
    grafico()
  elif opcao == 7:
    descricao()
  elif opcao == 8:
    configuracoes()
  else:
    print("="*16)
    print("Volte sempre! :)")
    break  

