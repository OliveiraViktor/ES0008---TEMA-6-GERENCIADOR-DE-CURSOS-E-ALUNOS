import json
import os

ARQUIVO_DADOS = "dados_academicos.json"

def salvar_dados(dados: dict, caminho: str = ARQUIVO_DADOS) -> None:
    """Serializa e guarda o dicionário de dados em formato JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def carregar_dados(caminho: str = ARQUIVO_DADOS) -> dict:
    """Lê e desserializa os dados do ficheiro JSON, retornando um dicionário vazio se não existir."""
    if not os.path.exists(caminho):
        return {}
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}