CREATE DATABASE escola;

USE escola;

CREATE TABLE alunos
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    idade INT
);

INSERT INTO alunos(nome, idade)
VALUES
('Maria',22),
('Pedro',20),
('José',18);