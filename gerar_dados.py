from faker import Faker
from random import *
from supabase import create_client, Client

fake = Faker('pt-br')

supabase_url = 'https://zcetblxoyequchygspyt.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpjZXRibHhveWVxdWNoeWdzcHl0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjMzNjM1OSwiZXhwIjoyMDU3OTEyMzU5fQ.pnzr79nS8daUcDAnB6wRZeotiT0hvHXqY7uV8jIorVc'
supabase: Client = create_client(supabase_url, supabase_key)

nome_alunos = []
nome_profs = []
ra = []
cursos = []
disc = []
tcc_titulo = []
disciplinas = [
    "Introdução à Computação", # Ciência da Computação
    "Física I", # Eletrica
    "Empreendedorismo",  # Administração
    "Introdução à Administração", # Administração
    "Cálculo Diferencial",  # Engenharia de Produção
    "Algoritmos",  # Ciência da Computação
    "Inteligência Artificial", # Ciência da Computação
    "Arquitetura de Computadores", # Ciência da Computação
    "Termodinâmica",  # Engenharia Mecânica
    "Resistência dos Materiais", # Engenharia Mecânic
    "Sistemas Digitais"  # Eletrica
]

disciplinas_curso = [
    "Ciência da Computação",
    "Engenharia Eletrica",
    "Administração",
    "Administração",
    "Engenharia de Produção",
    "Ciência da Computação",
    "Ciência da Computação",
    "Ciência da Computação",
    "Engenharia Mecânica",
    "Engenharia Mecânica",
    "Engenharia Eletrica"
]

cursos = [
    "Engenharia Mecânica",
    "Administração",
    "Engenharia de Produção",
    "Ciência da Computação",
    "Engenharia Eletrica"
]

# Nomes

# verificar se já existem alunos no banco
resposta_aluno = supabase.table("alunos").select("nome").execute()
if len(resposta_aluno.data) == 0:
    for i in range(15):
        nome = fake.name()
        nome_alunos.insert(i, nome)

    dados_nome = []
    for n in nome_alunos:
        dados_nome.append({"nome": n})

    supabase.table("alunos").insert(dados_nome).execute()
    print("Alunos inseridos")

## Professor
resposta_prof = supabase.table("professor").select("nome").execute()
if len(resposta_prof.data) == 0:
    for i in range(15):
        nome = fake.name()
        nome_profs.insert(i, nome)

    dados_nome_prof = []
    for n in nome_profs:
        dados_nome_prof.append({"nome": n})

    supabase.table("professor").insert(dados_nome_prof).execute()
    print("Professores inseridos")

## Disciplina
resposta_disc = supabase.table("disciplina").select("nome").execute()
if len(resposta_disc.data) == 0:
    dados_disc = []
    for i in range(len(disciplinas)):
        dados_disc.append({"nome": disciplinas[i], "curso": disciplinas_curso[i]})
    supabase.table("disciplina").insert(dados_disc).execute()
    print("Disciplinas inseridas")

## Cursos
resposta_curso = supabase.table("curso").select("nome").execute()
if len(resposta_curso.data) == 0:
    dados_cursos = []
    for i in range(len(cursos)):
        dados_cursos.append({"nome": cursos[i]})
        
    supabase.table("curso").insert(dados_cursos).execute()
    print("Cursos inseridos")

## Matriz Curricular
# curso
# codigo
# semestre
resposta_matriz = supabase.table("matrizcurricular").select("curso_id").execute()
if len(resposta_matriz.data) == 0:
    dados_matriz = []
    
    resposta_cursos = supabase.table("curso").select("curso", "nome").execute()
    resposta_disciplina = supabase.table("disciplina").select("codigo_disciplina", "nome", "curso").execute()
    
    for curso in resposta_cursos.data:
        curso_id = curso["curso"]  

        for disc in resposta_disciplina.data:
            if disc["curso"] == "Ciência da Computação" or disc["curso"] == "Administração" :
                semestre = randint(1, 8)
                cod = disc["codigo_disciplina"]

                dados_matriz.append({
                    "curso_id": curso_id,
                    "codigo_id": cod,
                    "semestre": semestre
                })

            elif "Engenharia" in disc["curso"]:
                semestre = randint(1, 10)
                cod = disc["codigo_disciplina"]

                dados_matriz.append({
                    "curso_id": curso_id,
                    "codigo_id": cod,
                    "semestre": semestre
                })

    supabase.table("matrizcurricular").insert(dados_matriz).execute()
    print("Matriz Curricular inserida")


## TCC
# titulo

# orientador

## TCC Alunos
# ra_tcc

# Historico Aluno
#  Historico Professor
