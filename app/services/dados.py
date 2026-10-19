import json
import os

CAMINHO_PADRAO = "app_dados.json"

def salvar_dados(cursos, turmas, caminho=CAMINHO_PADRAO):
    """Salva cursos e turmas em arquivo JSON."""
    dados = {
        "cursos": [c.to_dict() for c in cursos],
        "turmas": [t.to_dict() for t in turmas]
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_dados(caminho=CAMINHO_PADRAO):
    """Carrega dados do arquivo JSON."""
    if not os.path.exists(caminho):
        return {"cursos": [], "turmas": []}
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)