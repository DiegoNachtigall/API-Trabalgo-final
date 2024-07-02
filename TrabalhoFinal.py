import requests
import matplotlib.pyplot as plt
import numpy as np

url_jogos = "http://localhost:3000/jogos"
url_usuarios = "https://api-trabalho-final.vercel.app/usuarios"
url_login = "http://localhost:3000/login"
# url_log = "https://api-trabalho-final.vercel.app/log"


def titulo(texto, sublinhado="-"):
  print()
  print(texto)
  print(sublinhado*40)

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
  token = usuario['token']
  
  print(f"Token: {token}")
  
else:
  print("Erro... Usuário ou senha inválidos")
  
  exit()

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
  print("==================================================================")

  response = requests.get(url_jogos)

  if response.status_code != 200:
    print("Erro... Não foi possível obter dados da API")
    return
  
  jogos = response.json()

  for jogo in jogos:
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

  novo_preco = float(input("Novo Preço R$: "))

  response = requests.put(url_jogos+"/"+str(id), 
                          json={"preco": novo_preco})
  
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

  print(f"Título do Jogo: {jogo[0]['titulo']}")
  print(f"Gênero.........: {jogo[0]['genero']}") 
  print(f"Preço R$.......: {jogo[0]['preco']:9.2f}")
  print()

  confirma = input("Confirma a Exclusão deste Jogo(S/N)? ").upper()

  if confirma == "S":
    response = requests.delete(url_jogos+"/"+str(id))
  
    if response.status_code == 200:
      print("Ok! Jogo Excluído com sucesso")
    else:
      print("Erro... Não foi possível excluir este jogo")

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

# --------------------------------------------- Programa Principal
while True:
  titulo("Cadastro de Jogos - Uso de API")
  print("1. Inclusão de Jogos")
  print("2. Listagem de Jogos")
  print("3. Alteração de Jogos")
  print("4. Exclusão de Jogos")
  print("5. Gráfico Comparando Gêneros")
  print("6. Finalizar")
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
    grafico()
  else:
    break  

