# Tarefas disponíveis

Todas as tarefas são executadas via `poetry run task <nome>`.

| Tarefa | Comando | Descrição |
|---|---|---|
| `test` | `pytest` | Executa todos os testes com cobertura |
| `test-unit` | `pytest tests/unit/ -v` | Apenas testes unitários |
| `lint` | `ruff check src/ tests/` | Verifica qualidade de código |
| `lint-fix` | `ruff check --fix src/ tests/` | Corrige problemas de lint automaticamente |
| `format` | `ruff format src/ tests/` | Formata o código-fonte |
| `format-check` | `ruff format --check src/ tests/` | Verifica formatação sem alterar arquivos |
| `quality` | `lint + format-check` | Lint + verificação de formatação |
| `dashboard` | `streamlit run ...` | Inicia o dashboard interativo |
| `docs` | `mkdocs serve` | Inicia servidor local da documentação |
| `docs-build` | `mkdocs build` | Gera a documentação estática em `site/` |
| `ci` | `quality + test` | Pipeline completo de CI |
