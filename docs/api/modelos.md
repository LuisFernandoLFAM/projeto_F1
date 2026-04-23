# Modelos

Modelos Pydantic que representam as entidades da OpenF1 API.

## Session

Representa uma sessão de F1 (treino livre, classificação ou corrida).

```python
from projeto_f1.models.session import Session
```

## Driver

Representa um piloto em uma sessão.

```python
from projeto_f1.models.driver import Driver
```

## Lap

Representa uma volta de um piloto.

```python
from projeto_f1.models.lap import Lap
```

## Stint

Representa um stint (período entre pit stops) de um piloto.

```python
from projeto_f1.models.stint import Stint
```
