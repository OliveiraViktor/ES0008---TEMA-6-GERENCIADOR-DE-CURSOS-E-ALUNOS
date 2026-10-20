class Curso:
    """Catálogo com as informações de um curso."""
    def __init__(self, codigo: str, nome: str, carga_horaria: int, pre_requisitos=None, ementa=""):
        self._codigo = codigo
        self._nome = nome
        self._carga_horaria = carga_horaria
        self._pre_requisitos = pre_requisitos or []
        self._ementa = ementa

    def __str__(self):
        return f"Curso: {self._nome} (Código: {self._codigo}) - {self._carga_horaria}h"

    def __repr__(self):
        return f"Curso(codigo='{self._codigo}', nome='{self._nome}')"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "carga_horaria": self.carga_horaria,
            "pre_requisitos": self.pre_requisitos
            }


class Oferta:
    """Classe base para ofertas acadêmicas."""
    def __init__(self, periodo_semestre, vagas):
        self._periodo_semestre = periodo_semestre
        self.vagas = vagas  # Aciona o setter para validação

    @property
    def vagas(self):
        return self._vagas

    @vagas.setter
    def vagas(self, valor):
        if valor < 0:
            raise ValueError("O número de vagas não pode ser negativo.")
        self._vagas = valor


class Turma(Oferta):
    """Representa uma turma específica de um curso, herda de Oferta."""
    def __init__(self, periodo_semestre, vagas, id_turma, codigo_curso, local):
        super().__init__(periodo_semestre, vagas)
        self.id_turma = id_turma
        self.codigo_curso = codigo_curso
        self.local = local
        self.dias_horarios = {}
        self.estado_aberta = False
        self.matriculas = [] 

    def abrir_turma(self):
        self.estado_aberta = True

    def fechar_turma(self):
        self.estado_aberta = False

    def adicionar_matricula(self, matricula):
        self.matriculas.append(matricula)

    def __len__(self):
        # Retorna a quantidade de alunos matriculados na turma
        return len(self.matriculas)


