drop table monitoracaoCiclo;
drop table tanque;
drop table funcionario;
drop table empresa;
drop table cargo;
drop table preco;
CREATE TABLE IF NOT EXISTS empresa(
	idEmpresa INT AUTO_INCREMENT PRIMARY KEY,
	nomeEmpresa varchar(255),
	cnpj char(14)
);
CREATE TABLE IF NOT EXISTS preco(
	idPreco int auto_increment primary key,
    dia date,
    preco decimal(3,2) 
);
CREATE TABLE IF NOT EXISTS cargo(
	idCargo int auto_increment primary key,
    cargo varchar(10)
);
CREATE TABLE IF NOT EXISTS funcionario (
	idFuncionario INT AUTO_INCREMENT PRIMARY KEY,
	nome VARCHAR(255),
	cpf VARCHAR(11),
	email VARCHAR(255),
	nasc date,
	genero CHAR(1),
	senha varchar(255),
	fkEmpresa INT,
	fkCargo INT,
    autenticacao boolean,
	FOREIGN KEY (fkEmpresa) REFERENCES empresa(idEmpresa),
    FOREIGN KEY (fkCargo) REFERENCES cargo(idCargo)
);
                
CREATE TABLE IF NOT EXISTS tanque (
	idTanque INT NOT NULL AUTO_INCREMENT,
	fkFuncionario INT,
    fkEmpresa INT,
	cep char(8),
	cidade varchar(255),
	bairro varchar(255),
	rua varchar(100),
	estado varchar(100),
	PRIMARY KEY (idTanque),
	FOREIGN KEY (fkFuncionario) REFERENCES funcionario (idFuncionario),
    FOREIGN KEY (fkEmpresa) REFERENCES empresa (idEmpresa)
);
                
CREATE TABLE IF NOT EXISTS monitoracaoCiclo (
	idMonitoracaoCiclo INT AUTO_INCREMENT PRIMARY KEY,
	idCiclo INT,
	diasRestante INT ,
	amonia DECIMAL(3,2),
	biomassa DECIMAL(5,2),
	dia DATE,
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
insert into cargo (cargo) values
('Analista'),
('Financeiro'),
('Administração')