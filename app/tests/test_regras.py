import pytest
import os
import json
from app.models.pessoas import Aluno
from app.models.academicos import Turma, Curso
from app.models.registros import Matricula
from app.services.regras_negocio import realizar_matricula, RegrasNegocioException
from app.services.dados import salvar_dados, carregar_dados


# ==========================================
# 1. TESTES DE CRIAÇÃO E MÉTODOS ESPECIAIS (SEMANAS 1 E 2)
# ==========================================

def test_01_criacao_curso_e_str():
    """Testa a criação de um Curso e a representação amigável __str__."""
    curso = Curso("ES101", "Engenharia de Software", 60)
    assert curso.codigo == "ES101"
    assert str(curso) == "Curso: Engenharia de Software (Código: ES101) - 60h"


def test_02_validacao_nota_matricula():
    """Testa o encapsulamento (@property) do atributo nota[cite: 3]."""
    mat = Matricula()
    mat.nota = 8.5
    assert mat.nota == 8.5
    
    with pytest.raises(ValueError, match="A nota deve estar entre 0 e 10."):
        mat.nota = 11


def test_03_validacao_frequencia_matricula():
    """Testa o encapsulamento (@property) do atributo frequência[cite: 3]."""
    mat = Matricula()
    mat.frequencia = 75
    assert mat.frequencia == 75
    
    with pytest.raises(ValueError, match="A frequência deve estar entre 0 e 100."):
        mat.frequencia = -5


def test_04_validacao_vagas_turma():
    """Garante que turmas não aceitem número de vagas negativo[cite: 3]."""
    with pytest.raises(ValueError, match="O número de vagas não pode ser negativo."):
        Turma("2026.1", -10, "T01", "ES101", "Sala 1")


def test_05_len_turma():
    """Testa o método especial __len__ na classe Turma para ocupação atual[cite: 4]."""
    turma = Turma("2026.1", 30, "T01", "ES101", "Sala 1")
    assert len(turma) == 0
    
    mat1 = Matricula(aluno_matricula="M001", id_turma="T01")
    mat2 = Matricula(aluno_matricula="M002", id_turma="T01")
    turma.adicionar_matricula(mat1)
    turma.adicionar_matricula(mat2)
    assert len(turma) == 2


def test_06_lt_aluno():
    """Testa o método especial __lt__ para ordenação por CR e desempate por nome[cite: 3]."""
    aluno1 = Aluno("Ana", "ana@email.com", "123", cr_atual=8.5)
    aluno2 = Aluno("Carlos", "carlos@email.com", "124", cr_atual=9.0)
    aluno3 = Aluno("Bruno", "bruno@email.com", "125", cr_atual=8.5)
    
    # Compara CR: 8.5 < 9.0
    assert aluno1 < aluno2
    # Empate no CR (8.5), desempata por ordem alfabética: "Ana" < "Bruno"
    assert aluno1 < aluno3


def test_07_eq_matricula():
    """Testa o método especial __eq__ para comparação única de matrículas[cite: 4]."""
    mat1 = Matricula(aluno_matricula="M001", id_turma="T01")
    mat2 = Matricula(aluno_matricula="M001", id_turma="T01")
    mat3 = Matricula(aluno_matricula="M002", id_turma="T01")
    
    assert mat1 == mat2
    assert mat1 != mat3


# ==========================================
# 2. TESTES DE REGRAS DE NEGÓCIO E RELACIONAMENTOS (SEMANA 3)
# ==========================================

def test_08_matricula_sucesso():
    """Testa o fluxo com sucesso da ligação Aluno ↔ Turma[cite: 3]."""
    aluno = Aluno("Lucas", "lucas@email.com", "M010")
    turma = Turma("2026.1", 10, "T01", "ES101", "Sala 1")
    
    mat = realizar_matricula(aluno, turma, [])
    assert len(turma) == 1
    assert mat.aluno_matricula == "M010"
    assert mat.id_turma == "T01"


def test_09_turma_lotada_rejeita_matricula():
    """Testa a rejeição de matrícula quando len(turma) == vagas[cite: 4]."""
    aluno1 = Aluno("Mariana", "mariana@email.com", "M011")
    aluno2 = Aluno("Pedro", "pedro@email.com", "M012")
    turma = Turma("2026.1", 1, "T01", "ES101", "Sala 1")  # Apenas 1 vaga

    realizar_matricula(aluno1, turma, [])
    assert len(turma) == 1

    with pytest.raises(RegrasNegocioException, match="lotada"):
        realizar_matricula(aluno2, turma, [])


def test_10_choque_horario_rejeita_matricula():
    """Testa a rejeição de matrícula por choque de horário no mesmo semestre[cite: 4]."""
    aluno = Aluno("Gabriel", "gabriel@email.com", "M013")
    
    # Duas turmas no mesmo dia e horário
    turma1 = Turma("2026.1", 30, "T01", "ES101", "Sala 1", dias_horarios={"ter": "10:00-12:00"})
    turma2 = Turma("2026.1", 30, "T02", "ES102", "Sala 2", dias_horarios={"ter": "10:00-12:00"})

    realizar_matricula(aluno, turma1, [])

    with pytest.raises(RegrasNegocioException, match="Choque de horário"):
        realizar_matricula(aluno, turma2, [turma1])


def test_11_semestres_diferentes_permite_mesmo_horario():
    """Garante que horários iguais em semestres distintos não gerem conflito[cite: 2]."""
    aluno = Aluno("Julia", "julia@email.com", "M014")
    
    turma_sem1 = Turma("2025.2", 30, "T01", "ES101", "Sala 1", dias_horarios={"ter": "10:00-12:00"})
    turma_sem2 = Turma("2026.1", 30, "T02", "ES102", "Sala 2", dias_horarios={"ter": "10:00-12:00"})

    realizar_matricula(aluno, turma_sem1, [])
    # Não deve lançar exceção
    realizar_matricula(aluno, turma_sem2, [turma_sem1])
    assert len(turma_sem2) == 1


# ==========================================
# 3. TESTES DE PERSISTÊNCIA EM JSON (SEMANA 3)
# ==========================================

def test_12_persistencia_salvar_e_carregar_json(tmp_path):
    """Testa a gravação e leitura dos dados em arquivo JSON[cite: 4]."""
    arquivo_teste = tmp_path / "dados_teste.json"
    
    curso = Curso("ES101", "Engenharia de Software", 60)
    aluno = Aluno("Fernanda", "fernanda@email.com", "M015")
    turma = Turma("2026.1", 20, "T01", "ES101", "Sala 1")
    matricula = Matricula("M015", "T01", nota=9.0, frequencia=100.0)

    # Salva
    salvar_dados([curso], [aluno], [turma], [matricula], caminho=str(arquivo_teste))
    assert os.path.exists(arquivo_teste)

    # Carrega e valida
    dados = carregar_dados(caminho=str(arquivo_teste))
    assert len(dados["cursos"]) == 1
    assert len(dados["alunos"]) == 1
    assert len(dados["turmas"]) == 1
    assert len(dados["matriculas"]) == 1
    assert dados["alunos"][0]["nome"] == "Fernanda"


def test_13_persistencia_arquivo_inexistente(tmp_path):
    """Garante retorno de estrutura vazia caso o arquivo JSON ainda não exista[cite: 4]."""
    caminho_falso = tmp_path / "nao_existe.json"
    dados = carregar_dados(caminho=str(caminho_falso))
    assert dados == {"cursos": [], "alunos": [], "turmas": [], "matriculas": []}


# ==========================================
# 4. TESTES DE LÓGICA DE DICIONÁRIO (SERIALIZAÇÃO)
# ==========================================

def test_14_to_dict_curso():
    """Valida a conversão do objeto Curso para dicionário[cite: 4]."""
    curso = Curso("ES102", "Banco de Dados", 60, pre_requisitos=["ES101"])
    d = curso.to_dict()
    assert d["codigo"] == "ES102"
    assert d["pre_requisitos"] == ["ES101"]


def test_15_to_dict_aluno():
    """Valida a conversão do objeto Aluno para dicionário[cite: 4]."""
    aluno = Aluno("Thiago", "thiago@email.com", "M016", cr_atual=7.8)
    d = aluno.to_dict()
    assert d["matricula"] == "M016"
    assert d["cr"] == 7.8