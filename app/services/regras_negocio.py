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

def realizar_matricula(aluno, turma, turmas_do_aluno=None, historico_aluno=None, curso_obj=None):
    """
    Efetua a matrícula validando vagas, choque de horário e pré-requisitos de forma segura.
    """
    if turmas_do_aluno is None:
        turmas_do_aluno = []
    if historico_aluno is None:
        historico_aluno = []

    # 1. Validação de Vagas
    if len(turma) >= turma.vagas:
        raise RegrasNegocioException(f"Turma {turma.id_turma} lotada.")

    # 2. Validação de Pré-requisitos (se aplicável)
    if curso_obj and hasattr(curso_obj, 'pre_requisitos'):
        for pre in curso_obj.pre_requisitos:
            if pre not in historico_aluno:
                raise RegrasNegocioException(f"Pré-requisito não cumprido: {pre}.")

    # 3. Validação de Choque de Horário
    for t_atual in turmas_do_aluno:
        if getattr(turma, 'periodo_semestre', None) == getattr(t_atual, 'periodo_semestre', None):
            if hasattr(turma, 'tem_conflito_horario') and turma.tem_conflito_horario(t_atual):
                raise RegrasNegocioException("Choque de horário detectado.")

    matricula = Matricula(aluno_matricula=aluno.matricula, id_turma=turma.id_turma)
    turma.adicionar_matricula(matricula)
    return matricula

def trancar_matricula(matricula):
    if getattr(matricula, 'estado', 'Ativa') != "Ativa":
        raise RegrasNegocioException("Apenas matrículas ativas podem ser trancadas.")
    matricula._estado = "Trancada"

def lancar_notas_frequencia(matricula, nota, frequencia):
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