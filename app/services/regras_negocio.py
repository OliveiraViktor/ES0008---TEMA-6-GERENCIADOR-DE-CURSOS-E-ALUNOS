import json
import os
from app.models.registros import Matricula

class RegrasNegocioException(Exception):
    pass

def carregar_configuracoes(caminho="settings.json"):
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"nota_minima_aprovacao": 6.0, "frequencia_minima_aprovacao": 75.0}

def realizar_matricula(aluno, turma, curso_da_turma, turmas_do_aluno, historico_aluno):
    """
    Efetua a matrícula verificando:
    1. Lotação de vagas
    2. Pré-requisitos cumpridos do curso
    3. Conflito de horários no mesmo semestre
    """
    # 1. Checagem de Vagas
    if len(turma) >= turma.vagas:
        raise RegrasNegocioException(f"Turma {turma.id_turma} lotada.")

    # 2. Checagem de Pré-requisitos
    # historico_aluno deve ser uma lista de códigos de cursos/disciplinas em que o aluno foi aprovado
    for pre in curso_da_turma.pre_requisitos:
        if pre not in historico_aluno:
            raise RegrasNegocioException(f"Pré-requisito não cumprido: {pre}.")

    # 3. Checagem de Choque de Horário
    for t_atual in turmas_do_aluno:
        if turma.periodo_semestre == t_atual.periodo_semestre:
            if turma.tem_conflito_horario(t_atual):
                raise RegrasNegocioException("Choque de horário detectado.")

    matricula = Matricula(aluno_matricula=aluno.matricula, id_turma=turma.id_turma)
    turma.adicionar_matricula(matricula)
    aluno.adicionar_matricula_ativa(matricula)
    return matricula

def trancar_matricula(matricula):
    """Realiza o trancamento de uma matrícula ativa."""
    if matricula.estado != "Ativa":
        raise RegrasNegocioException("Apenas matrículas ativas podem ser trancadas.")
    matricula._estado = "Trancada"

def lancar_notas_frequencia(matricula, nota, frequencia):
    """Lança nota e frequência e calcula automaticamente a situação final."""
    matricula.nota = nota
    matricula.frequencia = frequencia
    
    config = carregar_configuracoes()
    nota_min = config.get("nota_minima_aprovacao", 6.0)
    freq_min = config.get("frequencia_minima_aprovacao", 75.0)

    if frequencia < freq_min:
        matricula._estado = "Reprovado por Frequência"
    elif nota < nota_min:
        matricula._estado = "Reprovado por Nota"
    else:
        matricula._estado = "Aprovado"