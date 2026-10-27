class Matricula:
    """Entidade associativa entre Aluno e Turma, gerindo nota e frequência."""
    def __init__(self, aluno_matricula="", id_turma="", nota=0.0, frequencia=0.0, estado="Ativa"):
        self._aluno_matricula = aluno_matricula
        self._id_turma = id_turma
        self.nota = nota
        self.frequencia = frequencia
        self._estado = estado

    @property
    def aluno_matricula(self):
        return self._aluno_matricula

    @property
    def id_turma(self):
        return self._id_turma

    @property
    def nota(self):
        return self._nota

    @nota.setter
    def nota(self, valor):
        if valor < 0 or valor > 10:
            raise ValueError("A nota deve estar entre 0 e 10.")
        self._nota = valor

    @property
    def frequencia(self):
        return self._frequencia

    @frequencia.setter
    def frequencia(self, valor):
        if valor < 0 or valor > 100:
            raise ValueError("A frequência deve estar entre 0 e 100.")
        self._frequencia = valor

    @property
    def estado(self):
        return self._estado

    def to_dict(self):
        return {
            "aluno_matricula": self._aluno_matricula,
            "id_turma": self._id_turma,
            "nota": self._nota,
            "frequencia": self._frequencia,
            "estado": self._estado
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Matricula":
        return cls(
            aluno_matricula=data["aluno_matricula"],
            id_turma=data["id_turma"],
            nota=data.get("nota", 0.0),
            frequencia=data.get("frequencia", 0.0),
            estado=data.get("estado", "Ativa")
        )

    def __eq__(self, outra):
        return isinstance(outra, Matricula) and self._aluno_matricula == outra.aluno_matricula and self._id_turma == outra.id_turma