## SKILL.md — Guia de Boas Práticas para Projetos Python em Engenharia de Dados

> Documento de referência para padronização de projetos Python no contexto de Engenharia de Dados.
> Aplica-se a pipelines, ETLs, APIs internas, scripts analíticos e bibliotecas de apoio.

---

## Sumário

1. [Gerenciamento de Ambiente e Dependências](#1-gerenciamento-de-ambiente-e-dependências)
2. [Estrutura do Projeto](#2-estrutura-do-projeto)
3. [Qualidade de Código](#3-qualidade-de-código)
4. [Testes](#4-testes)
5. [Documentação](#5-documentação)
6. [Boas Práticas Gerais de Python](#6-boas-práticas-gerais-de-python)
7. [Integração Contínua](#7-integração-contínua)
8. [Convenções do Time](#8-convenções-do-time)

---

## 1. Gerenciamento de Ambiente e Dependências

### Regra fundamental

**Utilize exclusivamente o [Poetry](https://python-poetry.org/) para gerenciar dependências e ambientes virtuais.**
Nunca utilize `pip install` diretamente em projetos gerenciados com Poetry. O `pip` quebra a rastreabilidade do `pyproject.toml` e do `poetry.lock`.

### Instalação do Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Comandos essenciais

| Ação                              | Comando                                      |
|-----------------------------------|----------------------------------------------|
| Instalar dependências do projeto  | `poetry install`                             |
| Adicionar dependência             | `poetry add pandas`                          |
| Adicionar dep. de desenvolvimento | `poetry add --group dev pytest ruff`         |
| Remover dependência               | `poetry remove pandas`                       |
| Atualizar e regenerar lock        | `poetry lock`                                |
| Executar script no env virtual    | `poetry run python src/meu_modulo/main.py`   |
| Abrir shell no env virtual        | `poetry shell`                               |
| Ver ambiente ativo                | `poetry env info`                            |

### Estrutura do `pyproject.toml`

```toml
[tool.poetry]
name = "meu-projeto"
version = "0.1.0"
description = "Pipeline de dados da área X"
authors = ["Time de Engenharia <eng@empresa.com>"]
readme = "README.md"
packages = [{ include = "meu_projeto", from = "src" }]

[tool.poetry.dependencies]
python = "^3.11"
pandas = "^2.2"
pydantic = "^2.7"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-cov = "^5.0"
ruff = "^0.4"
mkdocs-material = "^9.5"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Regras

- O arquivo `poetry.lock` **deve ser versionado** no repositório.
- Nunca edite o `poetry.lock` manualmente.
- Ambientes virtuais devem ficar **dentro do projeto** (configure `poetry config virtualenvs.in-project true`).
- Separe dependências de produção das de desenvolvimento usando grupos (`--group dev`).

---

## 2. Estrutura do Projeto

### Padrão src-layout

Adote o padrão `src/` para isolar o código-fonte instalável do restante do projeto. Isso evita importações acidentais e melhora a reprodutibilidade dos testes.

### Estrutura recomendada

```
meu-projeto/
├── src/
│   └── meu_projeto/
│       ├── __init__.py
│       ├── config.py           # Configurações e variáveis de ambiente
│       ├── models/             # Modelos de dados (Pydantic, dataclasses)
│       │   └── __init__.py
│       ├── ingestion/          # Módulos de ingestão de dados
│       │   └── __init__.py
│       ├── transformation/     # Módulos de transformação
│       │   └── __init__.py
│       ├── storage/            # Módulos de persistência (DB, S3, etc.)
│       │   └── __init__.py
│       └── utils/              # Utilitários genéricos e helpers
│           └── __init__.py
├── tests/
│   ├── conftest.py             # Fixtures compartilhadas
│   ├── unit/
│   │   ├── test_ingestion.py
│   │   └── test_transformation.py
│   └── integration/
│       └── test_pipeline.py
├── docs/
│   └── index.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── poetry.lock
├── mkdocs.yml
├── README.md
├── SKILL.md
└── .env.example
```

### Princípios de modularização

- **Separação por domínio**: cada subpacote representa uma responsabilidade clara (`ingestion`, `transformation`, `storage`).
- **Baixo acoplamento**: módulos não devem depender diretamente uns dos outros; use interfaces/abstrações quando necessário.
- **Alta coesão**: funções e classes dentro de um módulo devem servir ao mesmo propósito.
- **Evite módulos "catch-all"**: nada de `utils.py` com 500 linhas. Divida por tema.

---

## 3. Qualidade de Código

### Ferramenta: Ruff

Utilize o [Ruff](https://docs.astral.sh/ruff/) como única ferramenta de lint e formatação. Ele substitui `flake8`, `isort`, `pyupgrade` e `black` com desempenho superior.

### Configuração no `pyproject.toml`

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
]
ignore = ["E501"]  # line-length já é controlado pela formatação

[tool.ruff.lint.isort]
known-first-party = ["meu_projeto"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Comandos

```bash
# Verificar problemas
poetry run ruff check src/ tests/

# Corrigir automaticamente o que for possível
poetry run ruff check --fix src/ tests/

# Formatar o código
poetry run ruff format src/ tests/

# Verificar formatação sem alterar (útil em CI)
poetry run ruff format --check src/ tests/
```

### Regras mínimas obrigatórias

- Sem imports não utilizados (`F401`).
- Sem variáveis não utilizadas (`F841`).
- Imports organizados pelo padrão isort (`I`).
- Sem uso de `==` para comparar com `None` ou `True`/`False` — use `is`.
- Comprimento máximo de linha: **100 caracteres**.

---

## 4. Testes

### Framework: pytest

Utilize exclusivamente o [pytest](https://docs.pytest.org/) como framework de testes.

### Cobertura mínima obrigatória: 50%

Projetos abaixo de 50% de cobertura não devem ter merges aprovados no branch principal.

### Configuração no `pyproject.toml`

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing --cov-fail-under=50"

[tool.coverage.run]
source = ["src"]
omit = ["*/__init__.py"]

[tool.coverage.report]
show_missing = true
```

### Boas práticas de testes unitários

**Nomenclatura:**
```python
# Padrão: test_<unidade>_<cenário>_<resultado_esperado>
def test_calcular_media_lista_vazia_retorna_zero():
    ...

def test_parse_data_formato_invalido_lanca_excecao():
    ...
```

**Isolamento com mocks:**
```python
from unittest.mock import MagicMock, patch

def test_buscar_dados_chama_api_uma_vez():
    with patch("meu_projeto.ingestion.cliente.requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"dados": []})
        resultado = buscar_dados(url="https://api.exemplo.com/dados")
        mock_get.assert_called_once()
```

**Fixtures no `conftest.py`:**
```python
# tests/conftest.py
import pytest
import pandas as pd

@pytest.fixture
def dataframe_exemplo():
    return pd.DataFrame({"id": [1, 2, 3], "valor": [10.0, 20.0, 30.0]})
```

**Regras:**
- Um teste deve verificar **uma única coisa**.
- Testes não devem depender de estado externo (banco de dados real, rede, filesystem) sem fixtures adequadas.
- Use `pytest.mark.parametrize` para cobrir múltiplos cenários sem duplicação.

```python
@pytest.mark.parametrize("entrada,esperado", [
    ([1, 2, 3], 2.0),
    ([0, 0, 0], 0.0),
    ([10], 10.0),
])
def test_calcular_media(entrada, esperado):
    assert calcular_media(entrada) == esperado
```

### Comandos

```bash
# Executar todos os testes
poetry run pytest

# Executar com relatório de cobertura em HTML
poetry run pytest --cov=src --cov-report=html

# Executar apenas testes unitários
poetry run pytest tests/unit/

# Executar testes com saída detalhada
poetry run pytest -v

# Parar na primeira falha
poetry run pytest -x
```

O relatório HTML é gerado em `htmlcov/index.html`.

---

## 5. Documentação

### Ferramenta: MkDocs + Material Theme

Utilize [MkDocs](https://www.mkdocs.org/) com o tema [Material](https://squidfunk.github.io/mkdocs-material/) para gerar documentação navegável e profissional.

### Configuração básica do `mkdocs.yml`

```yaml
site_name: Meu Projeto — Documentação
site_description: Pipeline de Engenharia de Dados
site_author: Time de Engenharia
repo_url: https://github.com/empresa/meu-projeto

theme:
  name: material
  language: pt-BR
  features:
    - navigation.tabs
    - navigation.sections
    - content.code.copy
  palette:
    - scheme: default
      primary: indigo
      accent: indigo

nav:
  - Início: index.md
  - Guia de Uso: usage.md
  - Arquitetura: architecture.md
  - Referência da API: api_reference.md
  - Contribuindo: contributing.md

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [src]

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
```

### Comandos

```bash
# Servir documentação localmente
poetry run mkdocs serve

# Gerar site estático
poetry run mkdocs build

# Publicar no GitHub Pages
poetry run mkdocs gh-deploy
```

### Docstrings — padrão Google Style

Utilize o padrão **Google Style** para docstrings. Seja consistente em todo o projeto.

```python
def calcular_media(valores: list[float]) -> float:
    """Calcula a média aritmética de uma lista de valores.

    Args:
        valores: Lista de números reais. Não pode ser vazia.

    Returns:
        A média aritmética dos valores fornecidos.

    Raises:
        ValueError: Se a lista estiver vazia.

    Examples:
        >>> calcular_media([1.0, 2.0, 3.0])
        2.0
    """
    if not valores:
        raise ValueError("A lista de valores não pode ser vazia.")
    return sum(valores) / len(valores)
```

### Regras de documentação

- Todo módulo público deve ter um docstring de nível de módulo.
- Toda função/método público deve ter docstring completo (args, returns, raises).
- Funções internas (prefixo `_`) podem ter docstrings simplificados.
- O `README.md` deve conter: propósito, instalação, uso básico e link para docs completos.

---

## 6. Boas Práticas Gerais de Python

### Tipagem com type hints

Type hints são **obrigatórios** em todas as assinaturas de funções e métodos públicos.

```python
from typing import Optional
from collections.abc import Generator

def ler_chunks(
    caminho: str,
    tamanho_chunk: int = 1000,
) -> Generator[list[dict], None, None]:
    ...

def buscar_usuario(user_id: int) -> Optional[dict]:
    ...
```

Use `from __future__ import annotations` para compatibilidade retroativa com Python 3.9.

### Logging ao invés de prints

**Nunca use `print()` em código de produção.** Use o módulo `logging`.

```python
import logging

logger = logging.getLogger(__name__)

def processar_arquivo(caminho: str) -> None:
    logger.info("Iniciando processamento do arquivo: %s", caminho)
    try:
        # lógica
        logger.debug("Arquivo processado com sucesso.")
    except FileNotFoundError:
        logger.error("Arquivo não encontrado: %s", caminho)
        raise
```

Configure o logger na entrada do programa (ex: `main.py`), não nos módulos internos.

### Tratamento adequado de exceções

```python
# Ruim — captura tudo e silencia erros reais
try:
    resultado = processar(dados)
except Exception:
    pass

# Correto — captura exceção específica e registra
try:
    resultado = processar(dados)
except ValueError as e:
    logger.warning("Dado inválido ignorado: %s", e)
    resultado = None
except ConnectionError as e:
    logger.error("Falha de conexão ao processar dados: %s", e)
    raise
```

- Nunca use `except Exception` sem registrar e re-lançar ou tratar explicitamente.
- Crie exceções customizadas para erros de domínio:

```python
class PipelineError(Exception):
    """Erro base para falhas no pipeline de dados."""

class SchemaValidationError(PipelineError):
    """Lançado quando os dados não passam na validação de schema."""
```

### Configurações via variáveis de ambiente

Use [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) para gerenciar configurações.

```python
# src/meu_projeto/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    api_key: str
    batch_size: int = 1000
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
```

Nunca faça `os.environ["MINHA_CHAVE"]` diretamente no código de negócio. Centralize em `config.py`.
Inclua `.env.example` no repositório e adicione `.env` ao `.gitignore`.

### Evitar código duplicado

- Extraia lógica repetida para funções utilitárias em `utils/`.
- Aplique o princípio **DRY** (Don't Repeat Yourself).
- Prefira composição a herança para reuso de comportamento.

### Princípios SOLID aplicados

| Princípio | Aplicação prática em Engenharia de Dados |
|-----------|------------------------------------------|
| **S** — Single Responsibility | Uma classe `Extractor` só extrai. Uma `Transformer` só transforma. |
| **O** — Open/Closed | Use classes base para readers; adicione novos formatos sem alterar o existente. |
| **L** — Liskov Substitution | Subclasses de `BaseReader` devem ser intercambiáveis. |
| **I** — Interface Segregation | Interfaces pequenas e específicas (`Readable`, `Writable`). |
| **D** — Dependency Inversion | Injete dependências (ex: conexão DB) em vez de instanciar dentro das classes. |

---

## 7. Integração Contínua

### Pipeline recomendado (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  quality:
    name: Lint e Testes
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalar Poetry
        uses: snok/install-poetry@v1
        with:
          version: "1.8.0"
          virtualenvs-in-project: true

      - name: Instalar dependências
        run: poetry install --no-interaction

      - name: Lint com Ruff
        run: |
          poetry run ruff check src/ tests/
          poetry run ruff format --check src/ tests/

      - name: Testes e Cobertura
        run: poetry run pytest --cov=src --cov-report=xml --cov-fail-under=50

      - name: Upload de cobertura
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
```

### Regras de proteção de branch

Configure no repositório GitHub:
- **Branch protection** em `main`: exige que o job `quality` passe antes do merge.
- Nenhum merge direto sem Pull Request.
- Ao menos 1 aprovação de revisão.

---

## 8. Convenções do Time

### Naming conventions

| Elemento          | Convenção       | Exemplo                         |
|-------------------|-----------------|---------------------------------|
| Variáveis         | `snake_case`    | `total_registros`               |
| Funções           | `snake_case`    | `calcular_media_movel()`        |
| Classes           | `PascalCase`    | `DataFrameTransformer`          |
| Constantes        | `UPPER_SNAKE`   | `MAX_RETRIES = 3`               |
| Módulos/pacotes   | `snake_case`    | `data_ingestion.py`             |
| Arquivos de teste | `test_*.py`     | `test_transformer.py`           |
| Métodos privados  | `_snake_case`   | `_validar_schema()`             |
| Tipos e Protocolos| `PascalCase`    | `DataSourceProtocol`            |

### Organização de imports

Siga a ordem definida pelo `isort` (configurado via Ruff):

```python
# 1. Biblioteca padrão
import os
import logging
from datetime import datetime
from typing import Optional

# 2. Bibliotecas de terceiros
import pandas as pd
from pydantic import BaseModel

# 3. Módulos internos do projeto
from meu_projeto.config import settings
from meu_projeto.utils.formatters import formatar_data
```

Nunca misture grupos. O Ruff aplicará automaticamente essa ordem.

### Padrão de commits — Conventional Commits

Formato: `<tipo>(<escopo opcional>): <descrição curta>`

| Tipo       | Uso                                               |
|------------|---------------------------------------------------|
| `feat`     | Nova funcionalidade                               |
| `fix`      | Correção de bug                                   |
| `docs`     | Alteração em documentação                         |
| `style`    | Formatação, sem alteração de lógica               |
| `refactor` | Refatoração sem adição de feature ou fix          |
| `test`     | Adição ou correção de testes                      |
| `chore`    | Tarefas de manutenção (CI, deps, configs)         |
| `perf`     | Melhoria de performance                           |

**Exemplos:**

```
feat(ingestion): adicionar suporte a leitura de arquivos Parquet
fix(transformation): corrigir cálculo de média com valores nulos
test(storage): adicionar testes unitários para o S3Writer
chore(deps): atualizar pandas para 2.2.1
docs: atualizar guia de instalação no README
```

Mensagens de commit devem estar em **português** e no **imperativo** (`adicionar`, `corrigir`, `atualizar`).

### Revisão de código (Code Review)

- Todo código que vai para `main` passa por Pull Request.
- O autor do PR é responsável por resolver os comentários antes do merge.
- Revisores devem verificar: lógica, testes, cobertura, nomenclatura e aderência a este guia.
- PRs devem ser atômicos: uma mudança por PR, sempre que possível.

---

## Referência Rápida — Comandos do Dia a Dia

```bash
# Instalar dependências
poetry install

# Adicionar nova lib
poetry add <pacote>

# Lint e formatação
poetry run ruff check --fix src/ tests/
poetry run ruff format src/ tests/

# Testes
poetry run pytest

# Testes com cobertura HTML
poetry run pytest --cov=src --cov-report=html

# Documentação local
poetry run mkdocs serve
```

---

*Documento mantido pelo time de Engenharia de Dados. Dúvidas e sugestões via Pull Request.*
