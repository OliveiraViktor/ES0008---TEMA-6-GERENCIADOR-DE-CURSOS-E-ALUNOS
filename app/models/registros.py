class Matricula:
    """Entidade associativa entre Aluno e Turma, gerindo nota e frequência."""
    def __init__(self, nota=0.0, frequencia=0.0, estado="Ativa"):
        self.nota = nota
        self.frequencia = frequencia
        self._estado = estado

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

    def __eq__(self, outra):
        return isinstance(outra, Matricula) and self.nota == outra.nota and self.frequencia == outra.frequenciaaclass Matricula:
    """Entidade associativa entre Aluno e Turma, gerindo nota e frequência."""
    def __init__(self, nota=0.0, frequencia=0.0, estado="Ativa"):
        self.nota = nota
        self.frequencia = frequencia
        self._estado = estado

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

    def __eq__(self, outra):
        return isinstance(outra, Matricula) and self.nota == outra.nota and self.frequencia == outra.frequencia