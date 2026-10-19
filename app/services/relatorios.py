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
                linhas.append(f"  - {aluno.nome} ({aluno._matricula})")
    return "\n".join(linhas)