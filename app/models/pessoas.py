class Pessoa:
    """Classe base para entidades do tipo pessoa."""
    def __init__(self, nome, email):
        self._nome = nome
        self._email = email

class Aluno(Pessoa):
    """Representa um aluno, herda de Pessoa e permite ordenação por CR."""
    def __init__(self, nome, email, matricula, cr_atual=0.0):
        super().__init__(nome, email)
        self._matricula = matricula
        self._historico = []
        self._cr = cr_atual

    @property
    def cr(self):
        return self._cr

    @property
    def nome(self):
        return self._nome

    def calcular_cr(self):
        pass

    def __lt__(self, outro):
        # Ordenação exigida na Semana 2: Compara primeiro o CR. 
        # Se houver empate, usa a ordem alfabética do nome.
        if self.cr == outro.cr:
            return self.nome < outro.nome
        return self.cr < outro.cr