from faker import Faker
import random
from supabase import create_client, Client

fake = Faker('pt-br')

supabase_url = 'https://qfmatgrmwoszwimeertc.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmbWF0Z3Jtd29zendpbWVlcnRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3Mjg0NTgsImV4cCI6MjA2MDMwNDQ1OH0.nb71wSHOVjuGrN9AvwYukni6aneAjDExqWhCPTE5inU'
supabase: Client = create_client(supabase_url, supabase_key)

nome_alunos = []
nome_profs = []
ra = []
cursos = []
disc = []
disciplinas = [
    "Introdução à Computação",  # Ciência da Computação
    "Física I",  # Eletrica
    "Empreendedorismo",  # Administração
    "Introdução à Administração",  # Administração
    "Cálculo Diferencial",  # Engenharia de Produção
    "Algoritmos",  # Ciência da Computação
    "Inteligência Artificial",  # Ciência da Computação
    "Arquitetura de Computadores",  # Ciência da Computação
    "Termodinâmica",  # Engenharia Mecânica
    "Resistência dos Materiais",  # Engenharia Mecânica
    "Sistemas Digitais"  # Eletrica
]

disciplinas_curso = [
    "Ciência da Computação", "Engenharia Eletrica", "Administração",
    "Administração", "Engenharia de Produção", "Ciência da Computação",
    "Ciência da Computação", "Ciência da Computação", "Engenharia Mecânica",
    "Engenharia Mecânica", "Engenharia Eletrica"
]

cursos = [
    "Engenharia Mecânica", "Administração", "Engenharia de Produção",
    "Ciência da Computação", "Engenharia Eletrica"
]

tcc_titulos = [
    "IA na Saúde: Desafios e Soluções", "Transformação Digital nas PMEs",
    "Gestão Sustentável Urbana", "Big Data em RH: Aplicações",
    "Educação Digital e Inclusão"
]

departamentos = ["Engenharia", "Computação", "Administração"]

# Alunos
resposta_aluno = supabase.table("alunos").select("nome", "ra").execute()
if len(resposta_aluno.data) == 0:  # verificar se já existem alunos no banco
    for i in range(40):
        nome = fake.name()
        nome_alunos.insert(i, nome)

    dados_nome = []
    for n in nome_alunos:
        dados_nome.append({"nome": n})

    supabase.table("alunos").insert(dados_nome).execute()
    print("Alunos inseridos")

## Professor
resposta_prof = supabase.table("professor").select("nome", "id_prof").execute()
if len(resposta_prof.data) == 0:
    for i in range(10):
        nome = fake.name()
        nome_profs.insert(i, nome)

    dados_nome_prof = []
    for n in nome_profs:
        dados_nome_prof.append({"nome": n})

    supabase.table("professor").insert(dados_nome_prof).execute()
    print("Professores inseridos")

## TCC
resposta_tcc = supabase.table("tcc").select("id_tcc", "titulo",
                                            "orientador").execute()
if len(resposta_tcc.data) == 0:
    dados_tcc = []
    resposta_professores = supabase.table("professor").select(
        "id_prof").execute()
    for tcc in tcc_titulos:

        professor_aleatorio = random.choice(resposta_professores.data)
        id_orientador = professor_aleatorio["id_prof"]
        dados_tcc.append({"titulo": tcc, "orientador": id_orientador})

    supabase.table("tcc").insert(dados_tcc).execute()
    print("TCCs inseridos")

## TCC Alunos
resposta_tcc_alunos = supabase.table("tccalunos").select(
    "ra_tcc", "id_tcc_aluno").execute()
if len(resposta_tcc_alunos.data) == 0:
    dados_tcc_alunos = []
    ra_alunos = supabase.table("alunos").select("ra").execute()
    id_tccs = supabase.table("tcc").select("id_tcc").execute()

    # lista com todos os alunos pra verificar depois se nn teve repetição de aluno
    alunos_disponiveis = []
    for aluno in ra_alunos.data:
        alunos_disponiveis.append(aluno["ra"])

    for id in id_tccs.data:
        # pegar 4 alunos para cada tcc
        for i in range(4):
            aluno_aleatorio = random.choice(alunos_disponiveis)
            dados_tcc_alunos.append({
                "ra_tcc": aluno_aleatorio,
                "id_tcc_aluno": id["id_tcc"]
            })
            alunos_disponiveis.remove(aluno_aleatorio)

    supabase.table("tccalunos").insert(dados_tcc_alunos).execute()
    print("TCC alunos inseridos")


## Disciplina
resposta_disciplina = supabase.table("disciplina").select(
    "codigo_disciplina", "nome", "curso").execute()
if len(resposta_disciplina.data) == 0:
    dados_disc = []
    for i in range(len(disciplinas)):
        dados_disc.append({
            "nome": disciplinas[i],
            "curso": disciplinas_curso[i]
        })
    supabase.table("disciplina").insert(dados_disc).execute()
    print("Disciplinas inseridas")

# Historico Aluno
resposta_historico_aluno = supabase.table("historico").select(
    "ra_aluno", "codigo", "semestre", "ano", "nota").execute()
if len(resposta_historico_aluno.data) == 0:

    dados_hist_aluno = []

    for aluno in resposta_aluno.data:

        disciplina_aleatoria = random.choice(resposta_disciplina.data)
        if disciplina_aleatoria[
                "curso"] == "Ciência da Computação" or disciplina_aleatoria[
                    "curso"] == "Administração":
            semestre = random.randint(1, 8)
        else:
            semestre = random.randint(1, 10)

        ano = random.randint(2000, 2010)
        nota = random.randint(0, 10)

        dados_hist_aluno.append({
            "ra_aluno":
            aluno["ra"],
            "codigo":
            disciplina_aleatoria["codigo_disciplina"],
            "semestre":
            semestre,  # ou aleatório
            "ano":
            ano,  # ou aleatório
            "nota":
            nota
        })

    supabase.table("historico").insert(dados_hist_aluno).execute()
    print("Historico do aluno inserido")


## Cursos
resposta_curso = supabase.table("curso").select("nome").execute()
if len(resposta_curso.data) == 0:
    dados_cursos = []
    for i in range(len(cursos)):
        prof = random.choice(resposta_prof.data)
        dados_cursos.append({
            "nome": cursos[i],
            "id_coordenador": prof["id_prof"]
        })

    supabase.table("curso").insert(dados_cursos).execute()
    print("Cursos inseridos")

## Matriz Curricular
resposta_matriz = supabase.table("matrizcurricular").select(
    "curso_id").execute()
if len(resposta_matriz.data) == 0:
    dados_matriz = []

    resposta_cursos = supabase.table("curso").select("curso", "nome").execute()

    for curso in resposta_cursos.data:
        curso_id = curso["curso"]

        for disc in resposta_disciplina.data:
            if disc["curso"] == "Ciência da Computação" or disc[
                    "curso"] == "Administração":
                semestre = random.randint(1, 8)
                cod = disc["codigo_disciplina"]

                dados_matriz.append({
                    "curso_id": curso_id,
                    "codigo_id": cod,
                    "semestre": semestre
                })

            elif "Engenharia" in disc["curso"]:
                semestre = random.randint(1, 10)
                cod = disc["codigo_disciplina"]

                dados_matriz.append({
                    "curso_id": curso_id,
                    "codigo_id": cod,
                    "semestre": semestre
                })

    supabase.table("matrizcurricular").insert(dados_matriz).execute()
    print("Matriz Curricular inserida")

resposta_professores = supabase.table("professor").select("id_prof").execute()
# Prof Departamento
resposta_departamento_prof = supabase.table("professor_departamento").select(
    "id_depto", "id_professor").execute()
if len(resposta_departamento_prof.data) == 0:

    dados_departamento_prof = []

    for prof in range(3):
        prof = random.choice(resposta_professores.data)
        dados_departamento_prof.append({"id_professor": prof["id_prof"]})

    supabase.table("professor_departamento").insert(
        dados_departamento_prof).execute()
    print("Professor Departamento inserido")

# Departamento
resposta_departamento = supabase.table("departamento").select("id", "nome").execute()
if len(resposta_departamento.data) == 0:

    dados_departamento = []
    idx = 0
    for prof in resposta_departamento_prof.data:
        dados_departamento.append({
            "id": prof["id_depto"],
            "nome": departamentos[idx]
        })
        idx += 1

    supabase.table("departamento").insert(dados_departamento).execute()
    print("Departamentos inserido")


# Leciona
resposta_leciona = supabase.table("leciona").select("semestre", "ano",
                                                    "periodo", "id_professor",
                                                    "codigo").execute()
if len(resposta_leciona.data) == 0:

    dados_leciona = []

    for prof in resposta_professores.data:
        materia = random.choice(resposta_disciplina.data)

        if materia["curso"] == "Ciência da Computação" or materia[
                "curso"] == "Administração":
            semestre = random.randint(1, 8)
        else:
            semestre = random.randint(1, 10)

        ano = random.randint(2000, 2010)
        periodos = ["noturno", "vespertino", "matutino"]

        dados_leciona.append({
            "semestre": semestre,
            "ano": ano,
            "periodo": random.choice(periodos),
            "id_professor": prof["id_prof"],
            "codigo": materia["codigo_disciplina"]
        })

    supabase.table("leciona").insert(dados_leciona).execute()
    print("Leciona inserida")
