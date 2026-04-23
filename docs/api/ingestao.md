# Ingestão

Clientes HTTP para consumir a OpenF1 API.

## Client base

`src/projeto_f1/ingestion/client.py` — cliente HTTP com retry e tratamento de erros.

## Endpoints disponíveis

### Sessions

```python
from projeto_f1.ingestion.sessions import fetch_sessions
```

### Drivers

```python
from projeto_f1.ingestion.drivers import fetch_drivers
```

### Laps

```python
from projeto_f1.ingestion.laps import fetch_laps
```

### Stints

```python
from projeto_f1.ingestion.stints import fetch_stints
```
