drop database algas;
create database algas;
use algas;

create table empresa(
  idEmpresa INT AUTO_INCREMENT PRIMARY KEY,
  nomeEmpresa varchar(255),
  email varchar(50),
  senha varchar(255),
  cnpj char(14)
);

CREATE TABLE funcionario (
  idFuncionario INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(255),
  cpf VARCHAR(11),
  email VARCHAR(255),
  idade INT(3),
  genero CHAR(1),
  senha varchar(255),
  fkEmpresa INT,
  funcao char(1),
  FOREIGN KEY (fkEmpresa) REFERENCES empresa(idEmpresa)
);


CREATE TABLE tanque (
  idTanque INT NOT NULL AUTO_INCREMENT,
  fkFuncionario INT,
  cep char(8),
  cidade varchar(100),
  bairro varchar(100),
  rua varchar(100),
  estado varchar(100),
  PRIMARY KEY (idTanque),
  FOREIGN KEY (fkFuncionario) REFERENCES funcionario (idFuncionario)
);


CREATE TABLE monitoracaoCiclo (
  idMonitoracaoCiclo INT AUTO_INCREMENT PRIMARY KEY,
  idCiclo INT,
  diasRestante INT ,
  amonia DECIMAL(3,2),
  biomassa DECIMAL(5,2),
  dias DATE,
  oxigenio DECIMAL(3,1),
  peso_peixe DECIMAL(7,1),
  ph DECIMAL(3,1),
  qualidade_agua DECIMAL(5,2),
  quantidade_peixe INT,
  salinidade DECIMAL(5,2),
  temperatura DECIMAL(5,2),
  turbidez DECIMAL(5,2),
  visibilidade DECIMAL(5,2),
  fkTanque INT,
  FOREIGN KEY (fkTanque) REFERENCES tanque (idTanque)
  );

  