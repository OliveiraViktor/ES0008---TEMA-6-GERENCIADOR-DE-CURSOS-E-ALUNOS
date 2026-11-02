import os
from app.models.pessoas import Aluno
from app.models.academicos import Curso, Turma
from app.models.registros import Matricula
from app.services.regras_negocio import realizar_matricula, trancar_matricula, lancar_notas_frequencia, RegrasNegocioException
from app.services.relatorios import calcular_taxa_aprovacao, distribuicao_notas, top_n_alunos
from app.services.dados import salvar_dados, carregar_dados

dados_iniciais = carregar_dados()
cursos = [Curso.from_dict(c) for c in dados_iniciais.get("cursos", [])]
alunos = [Aluno.from_dict(a) for a in dados_iniciais.get("alunos", [])]
turmas = [Turma.from_dict(t) for t in dados_iniciais.get("turmas", [])]
matriculas = [Matricula.from_dict(m) for m in dados_iniciais.get("matriculas", [])]  

def exibir_menu():
    print("\n========================================")
    print("    SISTEMA DE GESTÃO ACADÉMICA   ")
    print("========================================")
    print("1. Registrar Aluno")
    print("2. Registrar Curso")
    print("3. Criar Turma")
    print("4. Realizar Matrícula")
    print("5. Listar Turmas e Relatório de Vagas")
    print("6. Lançar Notas e Frequência")
    print("7. Trancar Matrícula")
    print("8. Relatórios Académicos")
    print("0. Sair")
    print("----------------------------------------")

def main():
    # Carregar dados persistidos ao iniciar
    dados = carregar_dados()
    
    alunos = [Aluno.from_dict(a) for a in dados.get("alunos", [])]
    cursos = [Curso.from_dict(c) for c in dados.get("cursos", [])]
    turmas = [Turma.from_dict(t) for t in dados.get("turmas", [])]
    
    # Coleta todas as matrículas ativas dentro das turmas para gerenciamento global
    def obter_todas_matriculas():
        todas = []
        for t in turmas:
            todas.extend(t.matriculas)
        return todas

    # Restaurar matrículas dentro das turmas a partir dos dados carregados
    for t_data in dados.get("turmas", []):
        turma_obj = next((t for t in turmas if t.id_turma == t_data["id_turma"]), None)
        if turma_obj:
            for m_data in t_data.get("matriculas", []):
                matricula_obj = Matricula.from_dict(m_data)
                turma_obj.adicionar_matricula(matricula_obj)
                aluno_obj = next((a for a in alunos if a.matricula == m_data["aluno_matricula"]), None)
                if aluno_obj:
                    aluno_obj.adicionar_matricula_ativa(matricula_obj)

    def persistir():
        # Coleta todas as matrículas atuais das turmas para salvar corretamente
        todas_matriculas = obter_todas_matriculas()
        salvar_dados(cursos, alunos, turmas, todas_matriculas)

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
            curso_turma = next((c for c in cursos if c.codigo == turma_escolhida.codigo_curso), None)

            try:
                # Monta a lista de turmas ativas do aluno para validação de conflito de horário
                turmas_do_aluno = []
                for t in turmas:
                    for m in t.matriculas:
                        if m.aluno_matricula == aluno_escolhido.matricula and m.estado == "Ativa":
                            turmas_do_aluno.append(t)

                # Histórico acadêmico do aluno (lista de códigos de cursos concluídos)
                historico_aluno = getattr(aluno_escolhido, 'historico', [])

                # CHAMADA: aluno, turma, turmas_do_aluno, historico_aluno, curso_obj
                realizar_matricula(
                    aluno=aluno_escolhido, 
                    turma=turma_escolhida, 
                    turmas_do_aluno=turmas_do_aluno, 
                    historico_aluno=historico_aluno, 
                    curso_obj=curso_turma
                )
                
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
                print("Matrículas:")
                if not t.matriculas:
                    print("  (Nenhuma matrícula nesta turma)")
                for m in t.matriculas:
                    aluno_nome = next((a.nome for a in alunos if a.matricula == m.aluno_matricula), m.aluno_matricula)
                    print(f"   • Aluno: {aluno_nome} (Mat: {m.aluno_matricula}) | Nota: {m.nota} | Frequência: {m.frequencia}% | Estado: {m.estado}")
                print("-" * 50)

        elif opcao == "6":
            print("\n--- Lançar Notas e Frequência ---")
            id_t = input("Digite o ID da turma: ").strip()
            turma_obj = next((t for t in turmas if t.id_turma == id_t), None)
            
            if not turma_obj:
                print("❌ Erro: Não há nenhuma turma cadastrada sob este código.")
                continue
            if not turma_obj.matriculas:
                print("❌ Esta turma existe, mas ainda não possui alunos matriculados.")
                continue
            
            print("Matrículas nesta turma:")
            for i, m in enumerate(turma_obj.matriculas):
                a_nome = next((a.nome for a in alunos if a.matricula == m.aluno_matricula), m.aluno_matricula)
                print(f"  [{i}] Aluno: {a_nome} | Estado Atual: {m.estado}")
            
            idx_m = int(input("Selecione o número da matrícula: "))
            mat_escolhida = turma_obj.matriculas[idx_m]
            
            nota = float(input("Digite a nota (0-10): "))
            frequencia = float(input("Digite a frequência (0-100%): "))
            
            try:
                lancar_notas_frequencia(mat_escolhida, nota, frequencia)
                persistir()
                print(f"✔ Notas lançadas! Nova situação do aluno: {mat_escolhida.estado}")
            except ValueError as e:
                print(f"❌ Erro de valor: {e}")

        elif opcao == "7":
            print("\n--- Trancar Matrícula ---")
            id_t = input("Digite o ID da turma: ").strip()
            turma_obj = next((t for t in turmas if t.id_turma == id_t), None)
            
            if not turma_obj:
                print("❌ Erro: Não há nenhuma turma cadastrada sob este código.")
                continue
            if not turma_obj.matriculas:
                print("❌ Esta turma existe, mas ainda não possui matrículas registradas.")
                continue
            
            print("Matrículas ativas nesta turma:")
            ativas = [m for m in turma_obj.matriculas if m.estado == "Ativa"]
            if not ativas:
                print("  (Nenhuma matrícula ativa nesta turma)")
                continue
            for i, m in enumerate(ativas):
                a_nome = next((a.nome for a in alunos if a.matricula == m.aluno_matricula), m.aluno_matricula)
                print(f"  [{i}] Aluno: {a_nome}")
                
            idx_m = int(input("Selecione o número da matrícula para trancar: "))
            mat_escolhida = ativas[idx_m]
            
            try:
                trancar_matricula(mat_escolhida)
                persistir()
                print("✔ Matrícula trancada com sucesso!")
            except RegrasNegocioException as e:
                print(f"❌ Erro de Negócio: {e}")

        elif opcao == "8":
            print("\n========================================")
            print("         RELATÓRIOS ACADÉMICOS          ")
            print("========================================")
            print("1. Taxa de Aprovação")
            print("2. Distribuição de Notas (Média, Mediana, Desvio Padrão)")
            print("3. Top N Alunos por CR")
            print("0. Voltar ao Menu Principal")
            
            op_rel = input("Escolha o relatório: ").strip()
            todas_m = obter_todas_matriculas()
            
            if op_rel == "1":
                id_turma_filtro = input("ID da turma (ou deixe em branco para global): ").strip()
                taxa = calcular_taxa_aprovacao(todas_m, id_turma=id_turma_filtro if id_turma_filtro else None)
                print(f"\n📈 Taxa de Aprovação: {taxa:.2f}%\n")
            elif op_rel == "2":
                id_turma_filtro = input("ID da turma (ou deixe em branco para global): ").strip()
                stats = distribuicao_notas(todas_m, id_turma=id_turma_filtro if id_turma_filtro else None)
                print(f"\n📊 Estatísticas de Notas:")
                print(f"   - Total de notas computadas: {stats['total']}")
                print(f"   - Média: {stats['media']}")
                print(f"   - Mediana: {stats['mediana']}")
                print(f"   - Desvio Padrão: {stats['desvio_padrao']}\n")
            elif op_rel == "3":
                try:
                    n = int(input("Digite o valor de N (ex: 3): "))
                except ValueError:
                    n = 3
                melhores = top_n_alunos(alunos, n=n)
                print(f"\n🏆 Top {n} Alunos por CR:")
                for idx, a in enumerate(melhores, 1):
                    print(f"   {idx}. {a.nome} - CR: {getattr(a, 'cr_atual', 0.0)}")
                print()

        elif opcao == "0":
            print("A encerrar o sistema. Até breve!")
            break
        else:
            print("⚠ Opção inválida. Por favor, escolha uma opção válida do menu.")

if __name__ == "__main__":
    main()