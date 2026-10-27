import os
from app.models.pessoas import Aluno
from app.models.academicos import Curso, Turma
from app.models.registros import Matricula
from app.services.regras_negocio import realizar_matricula, RegrasNegocioException
from app.services.dados import salvar_dados, carregar_dados

def exibir_menu():
    print("\n========================================")
    print("    SISTEMA DE GESTÃO ACADÉMICA (CLI)   ")
    print("========================================")
    print("1. Registrar Aluno")
    print("2. Registrar Curso")
    print("3. Criar Turma")
    print("4. Realizar Matrícula")
    print("5. Listar Turmas e Relatório de Vagas")
    print("0. Sair")
    print("----------------------------------------")

def main():
    # Carregar dados persistidos ao iniciar
    dados = carregar_dados()
    
    alunos = [Aluno.from_dict(a) for a in dados.get("alunos", [])]
    cursos = [Curso.from_dict(c) for c in dados.get("cursos", [])]
    turmas = [Turma.from_dict(t) for t in dados.get("turmas", [])]

    # Restaurar matrículas dentro das turmas a partir dos dados carregados
    for t_data in dados.get("turmas", []):
        turma_obj = next((t for t in turmas if t.id_turma == t_data["id_turma"]), None)
        if turma_obj:
            for m_data in t_data.get("matriculas", []):
                matricula_obj = Matricula.from_dict(m_data)
                turma_obj.adicionar_matricula(matricula_obj)
                # Associar também ao aluno correspondente
                aluno_obj = next((a for a in alunos if a.matricula == m_data["aluno_matricula"]), None)
                if aluno_obj:
                    aluno_obj.adicionar_matricula_ativa(matricula_obj)

    def persistir():
        dados_dict = {
            "alunos": [a.to_dict() for a in alunos],
            "cursos": [c.to_dict() for c in cursos],
            "turmas": [t.to_dict() for t in turmas]
        }
        salvar_dados(dados_dict)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- Registo de Aluno ---")
            mat = input("Número de matrícula: ")
            nome = input("Nome completo: ")
            email = input("E-mail institucional: ")
            cr = float(input("CR inicial (ex: 0.0): ") or 0.0)
            
            if any(a.matricula == mat for a in alunos):
                print("❌ Erro: Já existe um aluno com esta matrícula.")
                continue
            
            novo_aluno = Aluno(matricula=mat, nome=nome, email=email, cr_atual=cr)
            alunos.append(novo_aluno)
            persistir()
            print("✔ Aluno registado e guardado com sucesso!")

        elif opcao == "2":
            print("\n--- Registo de Curso ---")
            cod = input("Código do curso: ")
            nome = input("Nome do curso: ")
            carga = int(input("Carga horária (horas): "))
            ementa = input("Ementa (opcional): ")
            
            if any(c.codigo == cod for c in cursos):
                print("❌ Erro: Já existe um curso com este código.")
                continue
            
            novo_curso = Curso(codigo=cod, nome=nome, carga_horaria=carga, ementa=ementa)
            cursos.append(novo_curso)
            persistir()
            print("✔ Curso registado e guardado com sucesso!")

        elif opcao == "3":
            if not cursos:
                print("⚠ Erro: Deve registar pelo menos um curso antes de criar turmas.")
                continue
            print("\n--- Criação de Turma ---")
            id_t = input("ID da Turma (ex: TURMA01): ")
            
            print("Cursos disponíveis:")
            for i, c in enumerate(cursos):
                print(f"  [{i}] {c.nome} (Código: {c.codigo})")
            idx_curso = int(input("Selecione o número do curso: "))
            
            semestre = input("Período/Semestre (ex: 2026.1): ")
            vagas = int(input("Capacidade máxima de vagas: "))
            local = input("Local/Sala: ")
            
            print("Configuração de Dias e Horários (Ex: Seg 10:00, Qua 10:00)")
            dias_horarios = {}
            while True:
                dia = input("Dia da semana (ex: Seg, ou Enter para terminar): ").strip()
                if not dia:
                    break
                horario = input(f"Horário para {dia} (ex: 10:00): ").strip()
                dias_horarios[dia] = horario

            curso_selecionado = cursos[idx_curso]
            nova_turma = Turma(
                periodo_semestre=semestre,
                vagas=vagas,
                id_turma=id_t,
                codigo_curso=curso_selecionado.codigo,
                local=local,
                dias_horarios=dias_horarios
            )
            turmas.append(nova_turma)
            persistir()
            print("✔ Turma criada e guardada com sucesso!")

        elif opcao == "4":
            if not alunos or not turmas:
                print("⚠ Erro: É necessário ter alunos e turmas registados para efetuar matrículas.")
                continue
            print("\n--- Efetuar Matrícula ---")
            print("Alunos:")
            for i, a in enumerate(alunos):
                print(f"  [{i}] {a.nome} (Mat: {a.matricula})")
            idx_a = int(input("Selecione o número do aluno: "))

            print("Turmas disponíveis:")
            for i, t in enumerate(turmas):
                ocupadas = len(t.matriculas)
                print(f"  [{i}] Turma {t.id_turma} | Semestre: {t.periodo_semestre} | Vagas: {ocupadas}/{t.vagas}")
            idx_t = int(input("Selecione o número da turma: "))

            aluno_escolhido = alunos[idx_a]
            turma_escolhida = turmas[idx_t]

            # Obter turmas atuais do aluno com matrículas ativas para validação de conflito
            turmas_do_aluno = []
            for t in turmas:
                for m in t.matriculas:
                    if m.aluno_matricula == aluno_escolhido.matricula and m.estado == "Ativa":
                        turmas_do_aluno.append(t)

            try:
                realizar_matricula(aluno_escolhido, turma_escolhida, turmas_do_aluno)
                persistir()
                print("✔ Matrícula realizada e guardada com sucesso!")
            except RegrasNegocioException as e:
                print(f"❌ Erro de Negócio: {e}")
            except ValueError as e:
                print(f"❌ Erro: {e}")

        elif opcao == "5":
            print("\n--- Relatório de Turmas e Vagas ---")
            if not turmas:
                print("Nenhuma turma registada.")
            for t in turmas:
                ocupadas = len(t.matriculas)
                print(f"Turma ID: {t.id_turma} | Semestre: {t.periodo_semestre} | Curso Cod: {t.codigo_curso} | Vagas: {ocupadas}/{t.vagas}")
                print(f"Local: {t._local} | Horários: {t.dias_horarios}")
                print("Matrículas Ativas:")
                if not t.matriculas:
                    print("  (Nenhuma matrícula nesta turma)")
                for m in t.matriculas:
                    aluno_nome = next((a.nome for a in alunos if a.matricula == m.aluno_matricula), m.aluno_matricula)
                    print(f"   • Aluno: {aluno_nome} (Mat: {m.aluno_matricula}) | Nota: {m.nota} | Frequência: {m.frequencia}% | Estado: {m.estado}")
                print("-" * 50)

        elif opcao == "0":
            print("A encerrar o sistema. Até breve!")
            break
        else:
            print("⚠ Opção inválida. Por favor, escolha uma opção válida do menu.")

if __name__ == "__main__":
    main()