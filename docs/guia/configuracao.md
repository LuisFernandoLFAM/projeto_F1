# Configuração

As configurações são carregadas via `pydantic-settings` a partir de variáveis de ambiente ou do arquivo `.env`.

## Variáveis disponíveis

| Variável | Padrão | Descrição |
|---|---|---|
| `OPENF1_BASE_URL` | `https://api.openf1.org/v1` | URL base da API |
| `DATA_DIR` | `data/` | Diretório de armazenamento local |
| `LOG_LEVEL` | `INFO` | Nível de log |

## Exemplo de `.env`

```dotenv
OPENF1_BASE_URL=https://api.openf1.org/v1
DATA_DIR=data/
LOG_LEVEL=DEBUG
```
