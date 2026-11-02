import statistics

def relatorio_alunos_por_turma(turma, alunos_dict):
    """Gera relatório textual de alunos matriculados na turma."""
    linhas = [
        f"--- Turma: {turma.id_turma} (Curso: {turma.codigo_curso}) ---",
        f"Período: {turma.periodo_semestre} | Vagas Ocupadas: {len(turma)}/{turma.vagas}",
        "Alunos Inscritos:"
    ]
    if not turma.matriculas:
        linhas.append("  Nenhum aluno matriculado.")
    else:
        for m in turma.matriculas:
            aluno = alunos_dict.get(m.aluno_matricula)
            if aluno:
                linhas.append(f"  - {aluno.nome} ({aluno.matricula})")
    return "\n".join(linhas)

def calcular_taxa_aprovacao(matriculas, id_turma=None):
    """Calcula a taxa de aprovação (%) global ou filtrada por turma."""
    if id_turma:
        m_filtradas = [m for m in matriculas if m.id_turma == id_turma]
    else:
        m_filtradas = matriculas
        
    if not m_filtradas:
        return 0.0
    
    aprovados = sum(1 for m in m_filtradas if getattr(m, 'estado', '') == "Aprovado")
    return (aprovados / len(m_filtradas)) * 100

def distribuicao_notas(matriculas, id_turma=None):
    """Calcula estatísticas (média, mediana, desvio padrão) das notas."""
    if id_turma:
        notas = [m.nota for m in matriculas if m.id_turma == id_turma and getattr(m, 'nota', None) is not None]
    else:
        notas = [m.nota for m in matriculas if getattr(m, 'nota', None) is not None]
        
    if not notas:
        return {"media": 0.0, "mediana": 0.0, "desvio_padrao": 0.0, "total": 0}
        
    media = statistics.mean(notas)
    mediana = statistics.median(notas)
    desvio = statistics.stdev(notas) if len(notas) > 1 else 0.0
    
    return {
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "desvio_padrao": round(desvio, 2),
        "total": len(notas)
    }

def top_n_alunos(alunos, n=5):
    """Retorna os Top N alunos ordenados por CR (utilizando o método __lt__ da classe Aluno)."""
    # Ordenação decrescente baseada na lógica implementada em __lt__ / __gt__
    alunos_ordenados = sorted(alunos, reverse=True)
    return alunos_ordenados[:n]

def listar_alunos_em_risco(matriculas, alunos_dict, nota_corte=6.0, freq_min=75.0):
    """Identifica alunos com nota parcial abaixo do corte ou frequência insuficiente."""
    riscos = []
    for m in matriculas:
        if getattr(m, 'estado', '') == "Ativa" or "Reprovado" in getattr(m, 'estado', ''):
            if (m.nota is not None and m.nota < nota_corte) or (m.frequencia is not None and m.frequencia < freq_min):
                aluno = alunos_dict.get(m.aluno_matricula)
                if aluno:
                    riscos.append({
                        "aluno": aluno,
                        "matricula_obj": m
                    })
    return riscos