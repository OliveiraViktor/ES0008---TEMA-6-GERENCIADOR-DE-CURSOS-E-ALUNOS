# ES0008 | TEMA 6: GERENCIADOR DE CURSOS E ALUNOS

### Este projeto foi criado a fim de desenvolver um sistema de linha de comandos (CLI) para gerir cursos, turmas, alunos e matrículas. O objetivo é aplicar conceitos de Programação Orientada a Objetos, como encapsulamento, herança, métodos especiais e validações rigorosas.


```
app/
├── main.py                # Ponto de entrada da CLI 
│
├── models/
│   ├── pessoas.py         # Classes: Pessoa, Aluno
│   ├── academicos.py      # Classes: Curso, Oferta, Turma
│   └── registros.py       # Classe: Matricula
│
├── services/
│   ├── regras_negocio.py  # Pré-requisitos, choques de horário, vagas e aprovação)
│   ├── relatorios.py      # Lógica matemática (taxa de aprovação, notas, Top N)
│   └── dados.py           # Módulo de persistência para salvar/carregar dados
│
├── cli/                   # Agrupa os subcomandos do terminal
│   ├── cursos_cmd.py      # Subcomandos (ex: acad cadastrar-curso)
│   ├── turmas_cmd.py      # Subcomandos (ex: acad abrir-turma)
│   ├── matriculas_cmd.py  # Subcomandos (ex: acad matricular, acad lancar-nota)
│   └── relatorios_cmd.py  # Subcomandos (ex: acad relatorio taxa-aprovacao)
│
├── tests/
│   └── test_regras.py     # Testes exigidos com pytest cobrindo os fluxos principais e erros
│
└── settings.json          # Ficheiro de configurações (nota_minima_aprovacao, data_limite_trancamento, etc.)

```