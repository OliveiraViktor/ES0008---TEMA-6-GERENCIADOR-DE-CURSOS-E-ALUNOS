class Oferta:
    """Classe base que representa uma oferta genérica no sistema."""
    pass

class Turma(Oferta):
    """
    Classe que herda de Oferta.
    Representa uma turma específica de um curso, incluindo dias/horários, local e controlo de vagas[cite: 1].
    """
    pass

class Curso:
    """
    Classe que representa um curso no catálogo.
    Conterá o código único, carga horária e a lista de pré-requisitos necessários[cite: 1].
    """
    pass