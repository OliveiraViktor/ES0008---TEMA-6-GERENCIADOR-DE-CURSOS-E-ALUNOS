import pytest
from app.models.pessoas import Aluno
from app.models.academicos import Turma, Curso
from app.models.registros import Matricula

def test_criacao_curso_e_str():
    curso = Curso("ES101", "Engenharia de Software", 60)
    assert str(curso) == "Curso: Engenharia de Software (Código: ES101) - 60h"

def test_validacao_nota_matricula():
    mat = Matricula()
    mat.nota = 8.5
    assert mat.nota == 8.5
    
    with pytest.raises(ValueError, match="A nota deve estar entre 0 e 10."):
        mat.nota = 11

def test_validacao_frequencia_matricula():
    mat = Matricula()
    mat.frequencia = 75
    assert mat.frequencia == 75
    
    with pytest.raises(ValueError, match="A frequência deve estar entre 0 e 100."):
        mat.frequencia = -5

def test_validacao_vagas_turma():
    with pytest.raises(ValueError, match="O número de vagas não pode ser negativo."):
        Turma("2024.1", -10, "T01", "ES101", "Sala 1")

def test_len_turma():
    turma = Turma("2024.1", 30, "T01", "ES101", "Sala 1")
    assert len(turma) == 0
    
    turma.adicionar_matricula(Matricula())
    turma.adicionar_matricula(Matricula())
    assert len(turma) == 2

def test_lt_aluno():
    aluno1 = Aluno("Ana", "ana@email.com", "123", cr_atual=8.5)
    aluno2 = Aluno("Carlos", "carlos@email.com", "124", cr_atual=9.0)
    aluno3 = Aluno("Bruno", "bruno@email.com", "125", cr_atual=8.5)
    
    # Compara CR: 8.5 < 9.0
    assert aluno1 < aluno2
    # Empate no CR (8.5), desempata pelo nome: "Ana" < "Bruno"
    assert aluno1 < aluno3