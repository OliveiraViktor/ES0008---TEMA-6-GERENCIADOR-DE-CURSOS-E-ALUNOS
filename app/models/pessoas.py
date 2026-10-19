class Pessoa:
    def __init__(self, nome, email):
        self._nome = nome
        self._email = email

class Aluno(Pessoa):
    def __init__(self, nome, email, matricula, cr_atual=0.0):
        super().__init__(nome, email)
        self._matricula = matricula
        self._historico = []  # Disciplinas cursadas
        self._matriculas_ativas = [] # Lista de matrículas ativas
        self._cr = cr_atual

    @property
    def matricula(self):
        return self._matricula

    @property
    def cr(self):
        return self._cr

    @property
    def nome(self):
        return self._nome

    @property
    def matriculas_ativas(self):
        return self._matriculas_ativas

    def adicionar_matricula_ativa(self, matricula):
        self._matriculas_ativas.append(matricula)

    def to_dict(self):
        return {
            "nome": self._nome,
            "email": self._email,
            "matricula": self._matricula,
            "cr": self._cr,
            "historico": self._historico
        }

    def __lt__(self, outro):
        if self.cr == outro.cr:
            return self.nome < outro.nome
        return self.cr < outro.cr