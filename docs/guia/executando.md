# Executando

## Dashboard

```bash
poetry run task dashboard
```

Acesse `http://localhost:8501` no navegador.

## Testes

```bash
# Todos os testes com cobertura
poetry run task test

# Apenas testes unitários
poetry run task test-unit
```

## Qualidade de código

```bash
# Lint
poetry run task lint

# Formatar
poetry run task format

# Lint + format (CI)
poetry run task quality
```

## Documentação

```bash
# Servidor local (hot reload)
poetry run task docs

# Build estático
poetry run task docs-build
```
