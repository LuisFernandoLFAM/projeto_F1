# Instalação

## Pré-requisitos

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)

## Instalação das dependências

```bash
# Dependências principais
poetry install

# Com dashboard Streamlit
poetry install --with dashboard

# Com documentação
poetry install --with docs

# Tudo junto
poetry install --with dashboard,docs
```

## Variáveis de ambiente

Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
cp .env.example .env
```
