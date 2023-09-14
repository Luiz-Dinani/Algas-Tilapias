class ResponseLoginModel:
    def __init__(self, idCliente, is2FaAtivo):
        self.idCliente = idCliente
        self.is2FaAtivo = is2FaAtivo

    def to_dict(self):
        return {
            'idCliente': self.idCliente,
            'is2FaAtivo': self.is2FaAtivo
        }