import json
import os

CAMINHO_PADRAO = "app_dados.json"

def salvar_dados(cursos, alunos, turmas, matriculas, caminho=CAMINHO_PADRAO):
    """Salva cursos, alunos, turmas e matrículas em arquivo JSON[cite: 4]."""
    dados = {
        "cursos": [c.to_dict() for c in cursos],
        "alunos": [a.to_dict() for a in alunos],
        "turmas": [t.to_dict() for t in turmas],
        "matriculas": [m.to_dict() for m in matriculas]
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_dados(caminho=CAMINHO_PADRAO):
    """Carrega todos os dados do arquivo JSON[cite: 4]."""
    if not os.path.exists(caminho):
        return {"cursos": [], "alunos": [], "turmas": [], "matriculas": []}
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)