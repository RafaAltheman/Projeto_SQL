CREATE TABLE IF NOT EXISTS alunos
(
  ra serial PRIMARY KEY,
  nome VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS professor
(
  id_prof serial PRIMARY KEY,
  nome VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS tcc
(
  id_tcc serial PRIMARY KEY,
  titulo VARCHAR(255),
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
  nome VARCHAR(255),
  curso text
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
  nome VARCHAR(30),
  id_coordenador int,
  FOREIGN KEY (id_coordenador) REFERENCES professor(id_prof)
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
  FOREIGN KEY (id) REFERENCES professor_departamento(id_depto),
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


/*1-Mostre todo o histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte */
/*
SELECT a.nome AS aluno, h.ra_aluno, d.nome AS disciplina, h.semestre, h.nota
FROM historico h
JOIN alunos a ON a.ra = h.ra_aluno
JOIN disciplina d ON d.codigo_disciplina = h.codigo
WHERE (h.ra_aluno, h.codigo) IN (
  SELECT h1.ra_aluno, h1.codigo
  FROM historico h1, historico h2
  WHERE h1.ra_aluno = h2.ra_aluno
    AND h1.codigo = h2.codigo
    AND CAST(h1.nota AS FLOAT) < 5
    AND CAST(h2.nota AS FLOAT) >= 5
)
ORDER BY a.nome, d.nome, h.ano, h.semestre;
*/
/*2-Mostre todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto  */
/*
SELECT 
  t.id_tcc, 
  t.titulo, 
  p.nome AS orientador, 
  STRING_AGG(a.nome, ', ') AS alunos
FROM tcc t
JOIN professor p ON t.orientador = p.id_prof
JOIN tccalunos ta ON t.id_tcc = ta.id_tcc_aluno
JOIN alunos a ON ta.ra_tcc = a.ra
GROUP BY t.id_tcc, t.titulo, p.nome
ORDER BY t.id_tcc;
*/
/*3-Mostre a matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum (e.g., Ciência da Computação e Ciência de Dados). Este exercício deve ser dividido em 2 queries sendo uma para cada curso */
/*
SELECT 
  c1.nome AS curso,
  d.nome AS disciplina
FROM matrizcurricular mc1
JOIN curso c1 ON mc1.curso_id = c1.curso
JOIN disciplina d ON mc1.codigo_id = d.codigo_disciplina
WHERE EXISTS (
  SELECT 1 
  FROM matrizcurricular mc2
  WHERE mc2.codigo_id = mc1.codigo_id
    AND mc2.curso_id != mc1.curso_id
);

SELECT 
  c2.nome AS curso,
  d.nome AS disciplina
FROM matrizcurricular mc2
JOIN curso c2 ON mc2.curso_id = c2.curso
JOIN disciplina d ON mc2.codigo_id = d.codigo_disciplina
WHERE EXISTS (
  SELECT 1 
  FROM matrizcurricular mc1
  WHERE mc1.codigo_id = mc2.codigo_id
    AND mc1.curso_id != mc2.curso_id
);
*/


/*4-Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno  */
/*
SELECT DISTINCT 
  a.nome AS aluno,
  h.codigo AS codigo_disciplina, 
  d.nome AS disciplina, 
  p.nome AS professor
FROM historico h
JOIN alunos a ON h.ra_aluno = a.ra
JOIN disciplina d ON h.codigo = d.codigo_disciplina
JOIN leciona l 
  ON l.codigo = h.codigo 
  AND l.ano = h.ano 
  AND CAST(h.semestre AS INT) = l.semestre
JOIN professor p ON l.id_professor = p.id_prof
ORDER BY a.nome, d.nome;
*/

/*5-Liste todos os chefes de departamento e coordenadores de curso em apenas uma query de forma que a primeira coluna seja o nome do professor, a segunda o nome do departamento coordena e a terceira o nome do curso que coordena. Substitua os campos em branco do resultado da query pelo texto "nenhum"*/
/*
SELECT 
  p.nome AS nome_professor,
  COALESCE(d.nome, 'nenhum') AS departamento,
  COALESCE(c.nome, 'nenhum') AS curso
FROM professor p
LEFT JOIN professor_departamento pd ON pd.id_professor = p.id_prof
LEFT JOIN departamento d ON d.id = pd.id_depto
LEFT JOIN curso c ON c.id_coordenador = p.id_prof
ORDER BY p.nome;
*/

/* mais 10 queires da lista */

/* 6- Encontre os nomes de todos os estudantes.  */
/*
SELECT nome FROM alunos;
*/
/* 7- Liste os IDs e nomes de todos os professores. */
/*
SELECT id_prof, nome FROM professor;
*/
/* 8- Encontre os nomes de todos os estudantes que cursaram "Física 1" */
/*
SELECT * FROM disciplina WHERE nome = 'Física 1';
SELECT a.nome
FROM alunos a
JOIN historico h ON a.ra = h.ra_aluno
JOIN disciplina d ON h.codigo = d.codigo_disciplina
WHERE d.nome LIKE '%Física%';
*/

/* 9 - Recupere os nomes e IDs dos estudantes que são orientados por um professor específico */
/*
SELECT 
  p.nome AS orientador,
  a.ra AS ra_aluno, 
  a.nome AS aluno
FROM tcc t
JOIN professor p ON t.orientador = p.id_prof
JOIN tccalunos ta ON t.id_tcc = ta.id_tcc_aluno
JOIN alunos a ON a.ra = ta.ra_tcc
ORDER BY p.nome, a.nome;
*/

/* 10 - Liste as disciplinas que são ministrados pelo professor , juntamente com os títulos dos cursos. */
/*
SELECT 
  p.nome AS professor,
  c.nome AS curso, 
  d.nome AS disciplina
FROM leciona l
JOIN professor p ON l.id_professor = p.id_prof
JOIN disciplina d ON l.codigo = d.codigo_disciplina
JOIN matrizcurricular mc ON mc.codigo_id = d.codigo_disciplina 
  AND mc.semestre::int = l.semestre
JOIN curso c ON c.curso = mc.curso_id
ORDER BY p.nome, c.nome, d.nome;
*/

/* 11 -  Liste os cursos que foram ministrados por mais de um professor em semestres diferentes. */
/*
SELECT DISTINCT 
  c.nome AS curso,
  p.nome AS professor,
  l1.semestre
FROM curso c
JOIN matrizcurricular mc ON c.curso = mc.curso_id
JOIN leciona l1 ON mc.codigo_id = l1.codigo
JOIN professor p ON l1.id_professor = p.id_prof
WHERE EXISTS (
    SELECT 1
    FROM matrizcurricular mc2
    JOIN leciona l2 ON mc2.codigo_id = l2.codigo
    WHERE mc2.curso_id = mc.curso_id
      AND mc2.codigo_id = mc.codigo_id
      AND (
        l2.id_professor != l1.id_professor OR
        l2.semestre != l1.semestre
      )
)
ORDER BY c.nome, l1.semestre;
*/

/* 12 - Liste os nomes dos estudantes que não cursaram nenhum curso no departamento de "Engenharia".*/
/*
SELECT a.nome
FROM alunos a
WHERE NOT EXISTS (
    SELECT 1
    FROM historico h
    JOIN leciona l ON h.codigo = l.codigo AND h.ano = l.ano AND h.semestre::int = l.semestre
    JOIN professor_departamento pd ON l.id_professor = pd.id_professor
    JOIN departamento d ON pd.id_depto = d.id
    WHERE h.ra_aluno = a.ra
      AND d.nome = 'Engenharia'
);
*/

/* 13 - Liste os professores que ministraram cursos com mais de 5 alunos matriculados. */
/*
SELECT 
  p.nome AS professor,
  COUNT(DISTINCT h.ra_aluno) AS total_alunos
FROM leciona l
JOIN professor p ON p.id_prof = l.id_professor
JOIN historico h ON h.codigo = l.codigo
GROUP BY p.nome
HAVING COUNT(DISTINCT h.ra_aluno) > 5
ORDER BY total_alunos DESC;
*/
/* 14 - Encontre os estudantes que cursaram tanto "Sistemas Digitais" quanto "Fisica I".*/
/*
SELECT a.nome AS aluno
FROM alunos a
WHERE EXISTS (
  SELECT 1
  FROM historico h
  JOIN disciplina d ON h.codigo = d.codigo_disciplina
  WHERE h.ra_aluno = a.ra
    AND d.nome = 'Sistemas Digitais'
)
AND EXISTS (
  SELECT 1
  FROM historico h
  JOIN disciplina d ON h.codigo = d.codigo_disciplina
  WHERE h.ra_aluno = a.ra
    AND d.nome = 'Física I'
);
*/
/* 15 - Recupere os nomes dos estudantes que são orientados por um professor que ensina "Sistemas Digitais"*/
/*
SELECT DISTINCT a.nome
FROM alunos a
JOIN tccalunos ta ON a.ra = ta.ra_tcc
JOIN tcc t ON ta.id_tcc_aluno = t.id_tcc
JOIN leciona l ON l.id_professor = t.orientador
JOIN disciplina d ON l.codigo = d.codigo_disciplina
WHERE d.nome = 'Sistemas Digitais';
*/
