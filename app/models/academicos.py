class Curso:
    """Catálogo com as informações de um curso."""
    def __init__(self, codigo, nome, carga_horaria, pre_requisitos=None, ementa=""):
        self._codigo = codigo
        self._nome = nome
        self._carga_horaria = carga_horaria
        self._pre_requisitos = pre_requisitos if pre_requisitos else []
        self._ementa = ementa

    @property
    def codigo(self):
        return self._codigo

    @property
    def nome(self):
        return self._nome

    @property
    def carga_horaria(self):
        return self._carga_horaria

    @property
    def pre_requisitos(self):
        return self._pre_requisitos

    @property
    def ementa(self):
        return self._ementa

    def to_dict(self):
        return {
            "codigo": self._codigo,
            "nome": self._nome,
            "carga_horaria": self._carga_horaria,
            "pre_requisitos": self._pre_requisitos,
            "ementa": self._ementa
        }

    def __str__(self):
        return f"Curso: {self._nome} (Código: {self._codigo}) - {self._carga_horaria}h"

    def __repr__(self):
        return f"Curso(codigo='{self._codigo}', nome='{self._nome}')"


class Oferta:
    """Classe base para ofertas acadêmicas."""
    def __init__(self, periodo_semestre, vagas):
        self._periodo_semestre = periodo_semestre
        self.vagas = vagas

    @property
    def periodo_semestre(self):
        return self._periodo_semestre

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
    def __init__(self, periodo_semestre, vagas, id_turma, codigo_curso, local, dias_horarios=None):
        super().__init__(periodo_semestre, vagas)
        self._id_turma = id_turma
        self._codigo_curso = codigo_curso
        self._local = local
        self._dias_horarios = dias_horarios if dias_horarios else {}
        self._estado_aberta = True
        self._matriculas = [] 

    @property
    def id_turma(self):
        return self._id_turma

    @property
    def codigo_curso(self):
        return self._codigo_curso

    @property
    def dias_horarios(self):
        return self._dias_horarios

    @property
    def matriculas(self):
        return self._matriculas

    def abrir_turma(self):
        self._estado_aberta = True

    def fechar_turma(self):
        self._estado_aberta = False

    def adicionar_matricula(self, matricula):
        self._matriculas.append(matricula)

    def tem_conflito_horario(self, outra_turma):
        """Verifica sobreposição de dias e horários com outra turma."""
        for dia, horario in self._dias_horarios.items():
            if dia in outra_turma.dias_horarios:
                if horario == outra_turma.dias_horarios[dia]:
                    return True
        return False

    def to_dict(self):
        return {
            "periodo_semestre": self._periodo_semestre,
            "vagas": self._vagas,
            "id_turma": self._id_turma,
            "codigo_curso": self._codigo_curso,
            "local": self._local,
            "dias_horarios": self._dias_horarios
        }

    def __len__(self):
        return len(self._matriculas)