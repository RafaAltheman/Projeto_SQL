from faker import Faker
import random
from supabase import create_client, Client

fake = Faker('pt-br')

supabase_url = ''
supabase_key = ''
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
    resposta_aluno = supabase.table("alunos").select("nome", "ra").execute()
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
    resposta_prof = supabase.table("professor").select("nome", "id_prof").execute()
    print("Professores inseridos")

## TCC
resposta_tcc = supabase.table("tcc").select("id_tcc", "titulo", "orientador").execute()
if len(resposta_tcc.data) == 0:
    dados_tcc = []
    resposta_professores = supabase.table("professor").select(
        "id_prof").execute()
    for tcc in tcc_titulos:

        professor_aleatorio = random.choice(resposta_professores.data)
        id_orientador = professor_aleatorio["id_prof"]
        dados_tcc.append({"titulo": tcc, "orientador": id_orientador})

    supabase.table("tcc").insert(dados_tcc).execute()
    resposta_tcc = supabase.table("tcc").select("id_tcc", "titulo", "orientador").execute()
    print("TCCs inseridos")

## TCC Alunos
resposta_tcc_alunos = supabase.table("tccalunos").select("ra_tcc", "id_tcc_aluno").execute()
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
    resposta_tcc_alunos = supabase.table("tccalunos").select("ra_tcc", "id_tcc_aluno").execute()
    print("TCC alunos inseridos")


## Disciplina
resposta_disciplina = supabase.table("disciplina").select("codigo_disciplina", "nome", "curso").execute()
if len(resposta_disciplina.data) == 0:
    dados_disc = []
    for i in range(len(disciplinas)):
        dados_disc.append({
            "nome": disciplinas[i],
            "curso": disciplinas_curso[i]
        })
    supabase.table("disciplina").insert(dados_disc).execute()
    resposta_disciplina = supabase.table("disciplina").select("codigo_disciplina", "nome", "curso").execute()
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
            "ra_aluno": aluno["ra"],
            "codigo": disciplina_aleatoria["codigo_disciplina"],
            "semestre": semestre, 
            "ano": ano,  
            "nota": nota
        })

    supabase.table("historico").insert(dados_hist_aluno).execute()
    resposta_historico_aluno = supabase.table("historico").select(
        "ra_aluno", "codigo", "semestre", "ano", "nota").execute()
    print("Historico do aluno inserido")


## Cursos
resposta_curso = supabase.table("curso").select("nome", "id_coordenador").execute()
if len(resposta_curso.data) == 0:
    dados_cursos = []
    for i in range(len(cursos)):
        prof = random.choice(resposta_prof.data)
        dados_cursos.append({
            "nome": cursos[i],
            "id_coordenador": prof["id_prof"]
        })

    supabase.table("curso").insert(dados_cursos).execute()
    resposta_curso = supabase.table("curso").select("nome", "id_coordenador").execute()
    print("Cursos inseridos")

## Matriz Curricular
resposta_matriz = supabase.table("matrizcurricular").select("curso_id", "codigo_id", "semestre").execute()
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
    resposta_matriz = supabase.table("matrizcurricular").select("curso_id", "codigo_id", "semestre").execute()
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

    supabase.table("professor_departamento").insert(dados_departamento_prof).execute()
    resposta_departamento_prof = supabase.table("professor_departamento").select(
        "id_depto", "id_professor").execute()
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
    resposta_departamento = supabase.table("departamento").select("id", "nome").execute()
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
    resposta_leciona = supabase.table("leciona").select("semestre", "ano",
        "periodo", "id_professor",
        "codigo").execute()
    print("Leciona inserida")


# Verificação dos dados inseridos 
print("\nValidação dos dados:")

# 1. Alunos tem que ter histórico
alunos_sem_historico = []
for aluno in resposta_aluno.data:
    tem_historico = False
    for hist in resposta_historico_aluno.data:
        if aluno["ra"] == hist["ra_aluno"]:
            tem_historico = True
            break
    if not tem_historico:
        alunos_sem_historico.append(aluno["nome"])
if alunos_sem_historico:
    print("Há alunos sem histórico")
else:
    print("Todos os alunos têm histórico")

# 2. Professores que não lecionam nenhuma disciplina
professores_sem_aula = []

for prof in resposta_prof.data:
    leciona_alguma = False
    for lec in resposta_leciona.data:
        if lec["id_professor"] == prof["id_prof"]:
            leciona_alguma = True
            break
    if not leciona_alguma:
        professores_sem_aula.append(prof["nome"])

if professores_sem_aula:
    print("Há professores que não estão lecionando")
else:
    print("Todos os professores estão lecionando pelo menos uma disciplina")

# 3. Disciplinas tem que estar em uma matriz curricular
disciplinas_sem_matriz = []

for disc in resposta_disciplina.data:
    esta_na_matriz = False
    for mc in resposta_matriz.data:
        if disc["codigo_disciplina"] == mc["codigo_id"]:
            esta_na_matriz = True
            break
    if not esta_na_matriz:
        disciplinas_sem_matriz.append(disc["nome"])
if disciplinas_sem_matriz:
    print("Há disciplinas que não estão em nenhuma matriz curricular")
else:
    print("Todas as disciplinas estão em pelo menos um curso.")

# 4. TCCs que não têm nenhum aluno
tccs_sem_aluno = []

for tcc in resposta_tcc.data:
    tem_aluno = False
    for ta in resposta_tcc_alunos.data:
        if tcc["id_tcc"] == ta["id_tcc_aluno"]:
            tem_aluno = True
            break
    if not tem_aluno:
        tccs_sem_aluno.append(tcc["titulo"])
if tccs_sem_aluno:
    print("Há TCCs sem nenhum aluno")
else:
    print("Todos os TCCs têm alunos participando.")

# 5. TCCs sem orientador válido
tccs_sem_orientador = []

for tcc in resposta_tcc.data:
    orientador_encontrado = False
    for prof in resposta_prof.data:
        if tcc["orientador"] == prof["id_prof"]:
            orientador_encontrado = True
            break
    if not orientador_encontrado:
        tccs_sem_orientador.append(tcc["titulo"])
if tccs_sem_orientador:
    print("Há TCCs sem orientador válido")
else:
    print("Todos os TCCs têm orientadores")

# 6. Departamentos sem professor (sem chefe)
departamentos_sem_chefe = []

for depto in resposta_departamento.data:
    tem_prof = False
    for pd in resposta_departamento_prof.data:
        if pd["id_depto"] == depto["id"]:
            tem_prof = True
            break
    if not tem_prof:
        departamentos_sem_chefe.append(depto["nome"])
if departamentos_sem_chefe:
    print("Há departamentos sem professor chefe")
else:
    print("Todos os departamentos têm professores vinculados")

# 7. Cursos sem coordenador válido
cursos_sem_coordenador = []

for curso in resposta_curso.data:
    coordenador_existe = False
    for prof in resposta_prof.data:
        if curso["id_coordenador"] == prof["id_prof"]:
            coordenador_existe = True
            break
    if not coordenador_existe:
        cursos_sem_coordenador.append(curso["nome"])
if cursos_sem_coordenador:
    print("Há cursos sem coordenador válido")
else:
    print("Todos os cursos têm coordenadores válidos")
