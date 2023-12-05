Drop table dim_empresa;
CREATE table dim_empresa(
	idEmpresa long,
	nomeEmpresa varchar(200),
	dt_cadastro datetime
);

Drop table dim_funcionario;
CREATE table dim_funcionario(
	idFuncionario long,
	idCargo int,
	idEmpresa long,
	nome varchar(200),
	dt_cadastro datetime
);

Drop table dim_tanque;
CREATE table dim_tanque (
	id_tanque long ,	
	idFuncionario long,
	estado char(2),
	cidade varchar(60),
	dt_cadastro datetime
);

DROP table dim_monitoracao;
CREATE table dim_monitoracao(
	idMonitoracao long,
	idTanque long,
	idCiclo int,
	dia date
);

Drop table fato_samaka;
CREATE table fato_samaka(
	idMonitoracao long,
	dia DATE,
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
	amonia decimal(3,2),
	preco decimal(4,2),
	pct_mortalidade decimal(7,4)
);

DROP table controle_atualizacao_dim_fatos;
CREATE TABLE controle_atualizacao_dim_fatos (
    idEnvio bigint PRIMARY KEY AUTO_INCREMENT,
    dt_envio DATETIME,
    idTabela INT,
    FOREIGN KEY (idTabela) REFERENCES tabelas_dw(idTabela)
);
TRUNCATE table controle_atualizacao_dim_fatos; 
insert into controle_atualizacao_dim_fatos (dt_envio, idTabela) values 
			(STR_TO_DATE('01/01/1900', '%d/%m/%Y'), 1),
			(STR_TO_DATE('01/01/1900', '%d/%m/%Y'), 2),
			(STR_TO_DATE('01/01/1900', '%d/%m/%Y'), 3),
			(STR_TO_DATE('01/01/1900', '%d/%m/%Y'), 4),
			(STR_TO_DATE('01/01/1900', '%d/%m/%Y'), 5);

DROP table tabelas_dw;
CREATE table tabelas_dw (
	idTabela int primary key auto_increment,
	nmTabela varchar(30)
);
INSERT INTO tabelas_dw(idTabela, nmTabela) values 
	(1, "dim_empresa"),
	(2, "dim_funcionario"),
	(3, "dim_tanque"),
	(4, "dim_monitoracao"),
	(5, "fato_samaka");

SELECT fnc_get_dt_atualizacao_tabela(1);

CALL  prc_resetar_dims_fato_controle(); 
CALL prc_inserir_dados_dim_fatos();
SELECT * from SamakaQtdItensDimsFato sqidf;
SELECT * from SamakaSnowFlakeView;

CREATE VIEW SamakaQtdItensDimsFato as
SELECT 
	COUNT(DISTINCT de.idEmpresa) as emp,
	COUNT(DISTINCT df.idFuncionario) as func,
	COUNT(DISTINCT dt.id_tanque) as tanque,
	COUNT(DISTINCT dm.idMonitoracao) as dim_monit,
	COUNT(DISTINCT fs.idMonitoracao) as ft_samaka
FROM dim_empresa de
LEFT JOIN dim_funcionario df ON de.idEmpresa = df.idEmpresa
LEFT JOIN dim_tanque dt on df.idFuncionario = dt.idFuncionario 
LEFT JOIN dim_monitoracao dm on dt.id_tanque = dm.idTanque
LEFT JOIN fato_samaka fs on dm.idMonitoracao = fs.idMonitoracao;

CREATE VIEW samaka.SamakaSnowFlakeView as
SELECT fs.*,
	   MAX(dm.idCiclo) as idCiclo, 
	   MAX(dt.id_tanque) as id_tanque, 
	   MAX(dt.estado) as estado, 
	   MAX(dt.cidade) as cidade, 
	   MAX(dt.dt_cadastro) as dt_cadastro_tanque,
	   MAX(df.idFuncionario) as idFuncionario,
	   MAX(df.idCargo) as idCargo,
	   MAX(df.nome) as nomeFunc,
	   MAX(df.dt_cadastro) as dt_cadastro_func,
	   MAX(de.idEmpresa) as idEmpresa,
	   MAX(de.nomeEmpresa) as nomeEmpresa,
	   MAX(de.dt_cadastro) as dt_cadastro_emp
from fato_samaka fs join dim_monitoracao dm on fs.idMonitoracao = dm.idMonitoracao 
				    JOIN dim_tanque dt on dm.idTanque = dt.id_tanque 
					JOIN dim_funcionario df on dt.idFuncionario = df.idFuncionario 
					JOIN dim_empresa de on df.idEmpresa = de.idEmpresa
GROUP BY fs.idMonitoracao;





