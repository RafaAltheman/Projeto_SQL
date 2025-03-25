from faker import Faker
from random import *
from supabase import create_client, Client
fake = Faker('pt-br')

supabase_url = 'https://zcetblxoyequchygspyt.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpjZXRibHhveWVxdWNoeWdzcHl0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjMzNjM1OSwiZXhwIjoyMDU3OTEyMzU5fQ.pnzr79nS8daUcDAnB6wRZeotiT0hvHXqY7uV8jIorVc'
supabase: Client = create_client(supabase_url, supabase_key)

nome_alunos = []
ra = []
cursos = []
disc = []
tcc_titulo = []

# verificar se já existem alunos no banco
resposta = supabase.table("alunos").select("nome").execute()

# --- Alunos --- #

if len(resposta.data) == 0:
    # Nomes
    for i in range(15):
        nome = fake.name()
        nome_alunos.insert(i, nome)
        
    dados_nome = [{"nome": nome} for nome in nome_alunos]
    supabase.table("alunos").insert(dados_nome).execute()
    
    # RA
    for i in range(15):
        ra_aluno = randint(10000000, 100000000)
        ra.insert(i, ra_aluno)

    dados_ra = [{"ra": nome} for nome in nome_alunos]
    supabase.table("ra").insert(dados_ra).execute()

    print("informações adc com sucesso")
else:
    print("ja esta com dados")
    
## Professor
# nome

## Disciplina
# nome
    
# codigo

## Cursos 
# nome

## Matriz Curricular
# curso

# codigo

# semestre

## TCC
# titulo
    
# orientador

## TCC Alunos
# ra_tcc

# historico aluno
