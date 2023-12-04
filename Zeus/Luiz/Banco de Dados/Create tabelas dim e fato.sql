Drop table dim_tanque;
CREATE table dim_tanque (
	id_tanque long ,	
	estado char(2),
	cidade varchar(60)
);

Drop table dim_funcionario;
CREATE table dim_funcionario(
	idFuncionario long,
	nome varchar(200),
	fkCargo int
);

Drop table dim_empresa;
CREATE table dim_empresa(
	idEmpresa long,
	nomeEmpresa varchar(200)
);

Drop table fato_negocio;
CREATE table fato_negocio (
	idEmpresa long,
	idTanque long,
	idPreco long,
	dia date,
	preco decimal(5,2)
);

Drop table fato_marketing;
CREATE table fato_marketing(
	IdPreco long,
	diasRestantes int,
	estado char(2)
);

Drop table fato_operacional;
CREATE table fato_operacional(
	idMonitoracao long,
	idTanque long,
	idFuncionario long,
	visibilidade decimal(4,1),
	turbidez decimal(4,1),
	temperatura int,
	salinidade decimal(4,1),
	quantidade_peixe int,
	qualidade_agua int,
	ph decimal(3,1),
	peso_peixe decimal(4,1),
	oxigenio decimal(3,1),
	biomassa decimal(4,1),
	amonia decimal(3,2)
);

CREATE table tabelas_dw (
	idTabela int primary key auto_increment,
	nmTabela varchar(30)
);

CREATE TABLE controle_atualizacao_dim_fatos (
    idEnvio bigint PRIMARY KEY AUTO_INCREMENT,
    data_envio DATE,
    idTabela INT,
    FOREIGN KEY (idTabela) REFERENCES tabelas_dw(idTabela)
);

CALL prc_insert_dim_fatos();

INSERT INTO dim_empresa 
		select idEmpresa, 
		 	   nomeEmpresa 
		FROM empresa emp
		WHERE emp.dt_cadastro >= fnc_get_dt_atualizacao_tabela(1);
	
SELECT fnc_get_dt_atualizacao_tabela(5);

SELECT *
		FROM preco, monitoracaoCiclo mc, tanque
		WHERE preco.dia >= DATE(fnc_get_dt_atualizacao_tabela(4)) AND 
			  mc.dia >= DATE(fnc_get_dt_atualizacao_tabela(4));
			 
			 
SELECT COALESCE(dt_envio, STR_TO_DATE('01/01/1900', '%d/%m/%Y'))     
    FROM controle_atualizacao_dim_fatos 
    WHERE idTabela = 4;
   
   SELECT COALESCE (dt_envio, '01/01/1900') from controle_atualizacao_dim_fatos cadf WHERE idTabela = 2; 
  
  
  SELECT * FROM monitoracaoCiclo mc WHERE idMonitoracaoCiclo = 892 and fkTanque = 2

  SELECT * from tanque t order by fkFuncionario ;
 
 INSERT into controle_atualizacao_dim_fatos (idTabela, dia) ctrl values ()  

