delimiter //
drop procedure proc_sheets;
create procedure proc_sheets (cod int)
begin
	declare funcao int;
	select fkCargo into funcao from funcionario where idFuncionario=cod;
    if funcao = 1 then
		select mon.*, funcao from monitoracaoCiclo mon join tanque tan on mon.fkTanque = tan.idTanque where tan.fkFuncionario=cod;
	elseif funcao = 2 then
		select mon.idMonitoracaoCiclo, mon.idCiclo, mon.diasRestante, mon.dia, mon.peso_peixe, mon.quantidade_peixe, mon.fkTanque, pre.preco, funcao
		from monitoracaoCiclo mon join preco pre on pre.dia = mon.dia join tanque tan on mon.fkTanque = tan.idTanque join funcionario fun on
		tan.fkEmpresa = fun.fkEmpresa where fun.idFuncionario=cod order by fkTanque asc;
	else
		select mon.*, pre.preco, fun.*, tan.*, car.cargo, funcao
		from monitoracaoCiclo mon join preco pre on pre.dia = mon.dia join tanque tan on mon.fkTanque = tan.idTanque join funcionario fun on
		tan.fkEmpresa = fun.fkEmpresa join cargo car on car.idCargo = fun.fkCargo where fun.idFuncionario=cod;
	end if;
end