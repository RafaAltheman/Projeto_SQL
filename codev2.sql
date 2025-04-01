CREATE TABLE IF NOT EXISTS alunos
(
  ra serial PRIMARY KEY,
  nome VARCHAR(30),
  curso int,
  FOREIGN KEY (curso) REFERENCES curso(curso)
);

CREATE TABLE IF NOT EXISTS professor
(
  id_prof serial PRIMARY KEY,
  nome VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS tcc
(
  id_tcc serial PRIMARY KEY,
  titulo VARCHAR(30),
  orientador int,
  FOREIGN KEY (orientador) REFERENCES professor(id_prof)
);

CREATE TABLE IF NOT EXISTS tccalunos
( 
  ra_tcc int,
  FOREIGN KEY (ra_tcc) REFERENCES alunos(ra),
  id_tcc_aluno int,
  FOREIGN KEY (id_tcc_aluno) REFERENCES tcc(id_tcc)
);

CREATE TABLE IF NOT EXISTS disciplina
(
  codigo_disciplina serial PRIMARY KEY,
  nome VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS historico
(
  ra_aluno int,
  FOREIGN KEY (ra_aluno) REFERENCES alunos(ra),
  codigo int,
  FOREIGN KEY (codigo) REFERENCES disciplina(codigo_disciplina),
  semestre VARCHAR(20),
  ano int,
  nota VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS curso
(
  curso serial PRIMARY KEY,
  nome VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS matrizcurricular
(
  curso_id int,
  FOREIGN KEY (curso_id) REFERENCES curso(curso),
  codigo_id int,
  FOREIGN KEY (codigo_id) REFERENCES disciplina(codigo_disciplina),
  semestre VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS professor_departamento
(
  id_professor int,
  FOREIGN KEY (id_professor) REFERENCES professor(id_prof),
  id_depto serial PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS departamento
(
  id int,
  FOREIGN KEY (id_depto) REFERENCES professor_departamento(id_depto),
  nome VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS leciona
(
  codigo int,
  FOREIGN KEY (codigo) REFERENCES disciplina(codigo_disciplina),
  id_professor int,
  FOREIGN KEY (id_professor) REFERENCES professor(id_prof),
  semestre int, 
  ano int, 
  periodo VARCHAR(30),
  PRIMARY KEY(semestre, ano, periodo)
);

/*1-Mostre todo o histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte*/
SELECT a.nome, h.ra_aluno, d.codigo_disciplina, d.nome AS disciplina, h.semestre, h.ano, h.nota
FROM historico h
JOIN disciplina d ON h.codigo = d.codigo_disciplina
JOIN alunos a ON h.ra_aluno = a.ra  
WHERE h.ra_aluno = 1
AND EXISTS (
    SELECT 1 
    FROM historico h2
    WHERE h2.ra_aluno = h.ra_aluno
    AND h2.codigo = h.codigo
    AND h2.nota = 'Reprovado'
)
ORDER BY h.ano, h.semestre;


/*2-Mostre todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto*/

SELECT t.id_tcc, t.titulo, p.nome AS orientador, a.nome AS aluno
FROM tcc t
JOIN professor p ON t.orientador = p.id_prof
JOIN tccalunos ta ON t.id_tcc = ta.id_tcc_aluno
JOIN alunos a ON ta.ra_tcc = a.ra
WHERE p.id_prof = 1;

/*3-Mostre a matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum (e.g., Ciência da Computação e Ciência de Dados). Este exercício deve ser dividido em 2 queries sendo uma para cada curso*/
SELECT mc1.curso_id, c1.nome AS curso, d.codigo_disciplina, d.nome AS disciplina
FROM matrizcurricular mc1
JOIN curso c1 ON mc1.curso_id = c1.curso
JOIN disciplina d ON mc1.codigo_id = d.codigo_disciplina
WHERE mc1.curso_id = 1
AND EXISTS (
    SELECT 1 
    FROM matrizcurricular mc2
    WHERE mc2.codigo_id = mc1.codigo_id
    AND mc2.curso_id = 2
);

SELECT mc2.curso_id, c2.nome AS curso, d.codigo_disciplina, d.nome AS disciplina
FROM matrizcurricular mc2
JOIN curso c2 ON mc2.curso_id = c2.curso
JOIN disciplina d ON mc2.codigo_id = d.codigo_disciplina
WHERE mc2.curso_id = 2
AND EXISTS (
    SELECT 1 
    FROM matrizcurricular mc1
    WHERE mc1.codigo_id = mc2.codigo_id
    AND mc1.curso_id = 1
);

/*4-Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno*/

SELECT h.codigo AS codigo_disciplina, d.nome AS disciplina, p.nome AS professor
FROM historico h
JOIN disciplina d ON h.codigo = d.codigo_disciplina
JOIN leciona l ON d.codigo_disciplina = l.codigo
JOIN professor p ON l.id_professor = p.id_prof
WHERE h.ra_aluno = 3;


/*5-Liste todos os chefes de departamento e coordenadores de curso em apenas uma query de forma que a primeira coluna seja o nome do professor, a segunda o nome do departamento coordena e a terceira o nome do curso que coordena. Substitua os campos em branco do resultado da query pelo texto "nenhum"*/



/*6- mais 10 queires da lista*/