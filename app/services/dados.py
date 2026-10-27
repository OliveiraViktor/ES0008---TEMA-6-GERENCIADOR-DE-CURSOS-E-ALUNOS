import json
import os

ARQUIVO_DADOS = "dados_academicos.json"

def salvar_dados(cursos, alunos, turmas, matriculas, caminho="dados_academicos.json"):
    dados = {
        "cursos": [c.to_dict() for c in cursos],
        "alunos": [a.to_dict() for a in alunos],
        "turmas": [t.to_dict() for t in turmas],
        "matriculas": [m.to_dict() for m in matriculas]
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_dados(caminho="dados_academicos.json"):
    # Se o ficheiro não existir, retorna a estrutura com listas vazias (exigido pelo teste 13)
    if not os.path.exists(caminho):
        return {
            "cursos": [],
            "alunos": [],
            "turmas": [],
            "matriculas": []
        }
    
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)