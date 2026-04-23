# OpenF1 API — Documentação Resumida

> Fonte: [https://openf1.org](https://openf1.org)

## Visão Geral

| Item | Detalhe |
|------|---------|
| URL base | `https://api.openf1.org/v1/` |
| Autenticação | Não necessária para dados históricos (2023+) |
| Tempo real | Requer assinatura paga |
| Formato padrão | JSON |
| Exportar CSV | Adicionar `?csv=true` à query |
| Chave especial | `latest` retorna o meeting/sessão mais recente |

### Filtros

Qualquer atributo numérico aceita operadores de comparação:

```
?speed>=315
?lap_duration<=90.5
?position<5
```

---

## Endpoints por Categoria

### Estrutura da Competição

| Endpoint | URL | Atualização |
|----------|-----|-------------|
| **Meetings** | `/v1/meetings` | Diária (meia-noite UTC) |
| **Sessions** | `/v1/sessions` | Diária (meia-noite UTC) |

**Meetings** — Fins de semana de GP ou testes. Cada meeting contém múltiplas sessões.

Campos principais: `meeting_key`, `meeting_name`, `meeting_official_name`, `country_code`, `location`, `date_start`, `circuit_key`, `year`

**Sessions** — Períodos de atividade na pista (treino livre, classificação, sprint, corrida).

Campos principais: `session_key`, `session_name`, `session_type`, `meeting_key`, `date_start`, `date_end`, `circuit_short_name`, `country_name`, `is_cancelled`

---

### Participantes

| Endpoint | URL | Obs |
|----------|-----|-----|
| **Drivers** | `/v1/drivers` | Por sessão |
| **Championship Drivers** | `/v1/championship_drivers` | Beta |
| **Championship Teams** | `/v1/championship_teams` | Beta |

**Drivers** — Informações do piloto em uma sessão específica.

Campos: `driver_number`, `full_name`, `name_acronym`, `broadcast_name`, `team_name`, `team_colour`, `headshot_url`, `session_key`

**Championship Drivers / Teams** — Classificação do campeonato de pilotos e construtores. Disponível por `session_key` para acompanhar a evolução ao longo do ano.

---

### Telemetria (alta frequência ~3.7 Hz)

| Endpoint | URL | Freq. |
|----------|-----|-------|
| **Car Data** | `/v1/car_data` | ~3.7 Hz |
| **Location** | `/v1/location` | ~3.7 Hz |

**Car Data** — Dados de telemetria do carro.

Campos: `driver_number`, `date`, `speed` (km/h), `rpm`, `n_gear`, `throttle` (%), `brake` (0 ou 100), `drs`

Valores DRS: `0/1` = desligado · `8` = elegível · `10/12/14` = ativado

**Location** — Coordenadas aproximadas do carro na pista.

Campos: `driver_number`, `date`, `x`, `y`, `z`, `session_key`

---

### Dados de Corrida

| Endpoint | URL | Descrição curta |
|----------|-----|-----------------|
| **Laps** | `/v1/laps` | Tempos de volta e setores |
| **Position** | `/v1/position` | Posição ao longo da sessão |
| **Intervals** | `/v1/intervals` | Gap para o carro à frente e para o líder |
| **Stints** | `/v1/stints` | Período de corrida por composto |
| **Pit** | `/v1/pit` | Dados de pit stops |
| **Overtakes** | `/v1/overtakes` | Trocas de posição |
| **Race Control** | `/v1/race_control` | Flags, safety car, incidentes |
| **Starting Grid** | `/v1/starting_grid` | Grid de largada |
| **Session Result** | `/v1/session_result` | Resultado final |

**Laps** — Detalhes de cada volta.

Campos: `driver_number`, `lap_number`, `lap_duration`, `duration_sector_1/2/3`, `i1_speed`, `i2_speed`, `st_speed`, `is_pit_out_lap`, `date_start`

**Position** — Histórico de posições durante a sessão (cada mudança gera um registro).

Campos: `driver_number`, `date`, `position`, `session_key`, `meeting_key`

**Intervals** — Atualizado a cada ~4 s durante a corrida.

Campos: `driver_number`, `date`, `interval` (gap ao carro à frente), `gap_to_leader`, `session_key`

**Stints** — Período de corrida contínuo por pneu.

Campos: `driver_number`, `stint_number`, `lap_start`, `lap_end`, `compound`, `tyre_age_at_start`, `session_key`

Compostos: `SOFT` · `MEDIUM` · `HARD` · `INTERMEDIATE` · `WET`

**Pit** — Informações de pit stops. Campo `stop_duration` disponível a partir do GP dos EUA 2024.

Campos: `driver_number`, `lap_number`, `pit_duration`, `stop_duration`, `date`, `session_key`

**Overtakes** — Trocas de posição (on-track, pit stops e penalidades). Dados podem ser incompletos.

Campos: `overtaking_driver_number`, `overtaken_driver_number`, `session_key`, `date`

**Race Control** — Comunicados da direção de prova.

Campos: `date`, `flag` (GREEN/YELLOW/RED/SC/VSC/CHEQUERED), `category` (Flag/SafetyCar/CarEvent/SessionStatus), `message`, `driver_number`, `lap_number`, `session_key`

**Starting Grid** — Grade de largada com tempos de classificação.

Campos: `driver_number`, `position`, `lap_duration`, `session_key`

**Session Result** — Classificação final com gaps e status (DNF/DNS/DSQ).

Campos: `driver_number`, `position`, `gap_to_leader`, `status`, `session_key`

---

### Outros

| Endpoint | URL | Atualização |
|----------|-----|-------------|
| **Team Radio** | `/v1/team_radio` | Seleção parcial |
| **Weather** | `/v1/weather` | A cada 1 minuto |

**Team Radio** — Áudios selecionados de rádio piloto–equipe (não é o registro completo).

Campos: `driver_number`, `date`, `recording_url`, `session_key`

**Weather** — Condições atmosféricas e de pista.

Campos: `date`, `air_temp` (°C), `track_temp` (°C), `humidity` (%), `pressure` (mbar), `rainfall` (bool), `wind_speed` (m/s), `wind_direction` (°), `meeting_key`, `session_key`

---

## Exemplos de uso em Python

```python
import requests

BASE = "https://api.openf1.org/v1"

# 1. Buscar a última sessão disponível
r = requests.get(f"{BASE}/sessions?session_key=latest")
sessao = r.json()[0]
print(sessao["session_name"], sessao["date_start"])

# 2. Tempos de volta de um piloto em uma sessão
r = requests.get(f"{BASE}/laps?session_key=9159&driver_number=1")
voltas = r.json()
for v in voltas:
    print(f"Volta {v['lap_number']}: {v['lap_duration']}s")

# 3. Telemetria de alta velocidade (>315 km/h)
r = requests.get(f"{BASE}/car_data?driver_number=55&session_key=9159&speed>=315")
telemetria = r.json()

# 4. Exportar voltas como CSV
r = requests.get(f"{BASE}/laps?session_key=9159&driver_number=1&csv=true")
with open("voltas.csv", "w") as f:
    f.write(r.text)
```

---

## Parâmetros comuns

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `session_key` | int / `latest` | Identifica a sessão |
| `meeting_key` | int / `latest` | Identifica o GP/fim de semana |
| `driver_number` | int | Número do piloto (1–99) |
| `year` | int | Ano do campeonato |
| `csv` | bool | `true` retorna CSV em vez de JSON |
