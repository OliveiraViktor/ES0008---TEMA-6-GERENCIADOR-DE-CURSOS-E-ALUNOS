class RegrasNegocioException(Exception):
    """Exceção para violações de regras acadêmicas."""
    pass

def realizar_matricula(aluno, turma, turmas_do_aluno):
    """
    Efetiva a matrícula de um aluno em uma turma validando:
    1. Se a turma está aberta e tem vagas.
    2. Se há choque de horário com outras turmas do aluno no mesmo semestre.
    """
    if len(turma) >= turma.vagas:
        raise RegrasNegocioException(f"Turma {turma.id_turma} lotada ({len(turma)}/{turma.vagas}).")

    for t_atual in turmas_do_aluno:
        if turma.periodo_semestre == t_atual.periodo_semestre:
            if turma.tem_conflito_horario(t_atual):
                raise RegrasNegocioException(f"Choque de horário com a turma {t_atual.id_turma}.")

    from app.models.registros import Matricula
    matricula = Matricula(aluno_matricula=aluno._matricula, id_turma=turma.id_turma)
    turma.adicionar_matricula(matricula)
    return matricula