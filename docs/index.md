# Projeto F1

Pipeline de dados de **Fórmula 1** consumindo a [OpenF1 API](https://openf1.org) com Python.

## Visão geral

Este projeto coleta, transforma e visualiza dados de corridas de F1 em tempo real ou histórico, incluindo:

- Sessões (treinos, classificação, corrida)
- Voltas e tempos por piloto
- Stints e estratégias de pneus
- Dashboard interativo com Streamlit

## Início rápido

```bash
# Instalar dependências
poetry install --with dashboard,docs

# Executar o dashboard
poetry run task dashboard

# Servir a documentação localmente
poetry run task docs
```

## Estrutura do projeto

```
src/projeto_f1/
├── config.py          # Configurações via variáveis de ambiente
├── models/            # Modelos Pydantic (Session, Driver, Lap, Stint)
├── ingestion/         # Clientes para a OpenF1 API
├── transformation/    # Transformações e agregações dos dados
├── storage/           # Persistência local
├── utils/             # Utilitários
└── dashboard/         # App Streamlit
```
