import os
import sqlite3 as db
# Funções


#Iniciar o Banco de Dados
agendadb = db.connect('agenda.db')
cur = agendadb.cursor()
  
#Criar as Tabelas
cur.execute('CREATE TABLE IF NOT EXISTS disciplina (nome varchar(40) PRIMARY KEY NOT NULL);')
cur.execute('CREATE TABLE IF NOT EXISTS atividade (nome varchar(40) NOT NULL, disciplina varchar(40), data_atividade text, concluida BIT NOT NULL DEFAULT 0, FOREIGN KEY (disciplina) REFERENCES disciplina(nome));')
agendadb.commit()


#Cadastrar uma Nova Disciplina

def adcionar_disciplina(Nome):
  checkDiscExiste = cur.execute("SELECT * FROM disciplina WHERE nome = ?", (Nome,))
  if checkDiscExiste.fetchone():
    print("ERRO: Já Existe uma Disciplina com esse nome")
  else:
    cur.execute("INSERT INTO disciplina VALUES (?)", (Nome, ))
    agendadb.commit()
    return print("Disciplina Adcionada com Sucesso")

#Cadastrar uma Nova Atividade em uma Disciplina

def adcionar_atividade(disciplina, nome, data):
  checkDiscExiste = cur.execute("SELECT * FROM disciplina WHERE nome = ?", (disciplina, ))
  if checkDiscExiste.fetchone():
    checkAtivNomeExiste = cur.execute("SELECT * FROM atividade WHERE nome = ? AND disciplina = ?", (nome, disciplina, ))
    if checkAtivNomeExiste.fetchone():
      return print("ERRO: Já existe uma atividade desta Disciplina com esse nome")
    checkAtivDataExiste = cur.execute("SELECT * FROM atividade WHERE disciplina = ? AND data_atividade = ?", (disciplina, data, ))
    if checkAtivDataExiste.fetchone():
      return print("ERRO: Já existe uma ativadade desta Disciplina nesta Data")
    cur.execute("INSERT INTO atividade (nome, disciplina, data_atividade) VALUES (?, ?, ?)", (nome, disciplina, data, ))
    agendadb.commit()
    return print("Atividade Adcionada com Sucesso")
  else:
    return print("ERRO: Essa Disciplina Não Existe")

  #Função para Marcar a Atividade como Concluida
def concluir_atividade(disciplina, nome):
  checkExiste = cur.execute("SELECT * FROM atividade WHERE nome = ? AND disciplina = ?", (nome, disciplina, ))
  if checkExiste.fetchone():
    cur.execute("UPDATE atividade SET pendente = 1 WHERE nome = ?", (nome, ))
    agendadb.commit()
    print("Atividade Marcada como Concluida!")
  else:
    print("ERRO: Atividade Não Existe")

#Listagagem das Diferentes Disciplinas
def listar_disciplina():
  disciplinas = cur.execute("SELECT * from Disciplina")
  print("")
  print('-'*20, "Disciplinas", '-'*20)
  for disciplina in disciplinas:
    print(f"""
{"-"*25}
Nome: {disciplina[0]}""")


#Listagem de Atividades de Acordo com a Pendência

def listar_atividades_pendencia(pendencia):
    atividades = cur.execute("SELECT nome, disciplina, data_atividade FROM atividade WHERE pendente = ?", (pendencia, ))
    print("")
    print(f"{'-'*25}Atividades{'-'*25}")
    for atividade in atividades:

      print(f"""
{"-"*25}
Nome: {atividade[0]}
Disciplina: {atividade[1]} 
Data: {atividade[2]}""")
  
