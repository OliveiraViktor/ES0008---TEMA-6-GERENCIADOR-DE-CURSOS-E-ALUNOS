from app.models.registros import Matricula

class RegrasNegocioException(Exception):
    pass

def realizar_matricula(aluno, turma, turmas_do_aluno):
    if len(turma) >= turma.vagas:
        raise RegrasNegocioException(f"Turma {turma.id_turma} lotada.")

    for t_atual in turmas_do_aluno:
        if turma.periodo_semestre == t_atual.periodo_semestre:
            if turma.tem_conflito_horario(t_atual):
                raise RegrasNegocioException("Choque de horário detectado.")

    # Cria a matrícula ligando Aluno ↔ Turma
    matricula = Matricula(aluno_matricula=aluno.matricula, id_turma=turma.id_turma)
    turma.adicionar_matricula(matricula) #a turma agora tem a matricula do aluno
    aluno.adicionar_matricula_ativa(matricula) #o aluno agora tem essa matricula ativa
    
    return matricula