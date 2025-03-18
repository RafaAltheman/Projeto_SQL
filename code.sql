CREATE TABLE IF NOT EXISTS alunos
(
  ra serial PRIMARY KEY,
  nome VARCHAR(30),
  id_curso int,
  FOREIGN KEY (id_curso) REFERENCES curso(curso)
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
  /* colocar limitacao de um orientador por tcc*/
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
  nome VARCHAR(30)
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

/*1-Mostre todo o histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte*/

/*2-Mostre todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto*/

/*3-Mostre a matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum (e.g., Ciência da Computação e Ciência de Dados). Este exercício deve ser dividido em 2 queries sendo uma para cada curso*/

/*4-Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno*/

/*5-Liste todos os chefes de departamento e coordenadores de curso em apenas uma query de forma que a primeira coluna seja o nome do professor, a segunda o nome do departamento coordena e a terceira o nome do curso que coordena. Substitua os campos em branco do resultado da query pelo texto "nenhum"*/

/*6- mais 10 queires da lista*/