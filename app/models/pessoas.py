class Pessoa:
    def __init__(self, nome: str, email: str):
        self._nome = nome
        self._email = email

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def email(self) -> str:
        return self._email


class Aluno(Pessoa):
    def __init__(self, nome: str, email: str, matricula: str, cr_atual: float = 0.0, historico: list = None):
        self._nome = nome
        self._email = email
        self._matricula = matricula
        self._cr = cr_atual
        self._historico = historico if historico is not None else []

    @property
    def matricula(self) -> str:
        return self._matricula

    @property
    def cr(self) -> float:
        return self._cr

    @property
    def matriculas_ativas(self) -> list:
        return self._matriculas_ativas

    def adicionar_matricula_ativa(self, matricula) -> None:
        self._matriculas_ativas.append(matricula)

    def to_dict(self) -> dict:
        return {
            "matricula": self._matricula,
            "nome": self._nome,
            "email": self._email,
            "cr": self._cr,
            "historico": self._historico
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Aluno":
        aluno = cls(
            matricula=data["matricula"],
            nome=data["nome"],
            email=data["email"],
            cr_atual=data.get("cr", 0.0)
        )
        aluno._historico = data.get("historico", [])
        return aluno

    def __lt__(self, outro: "Aluno") -> bool:
        if self.cr == outro.cr:
            return self.nome < outro.nome
        return self.cr < outro.cr