# Connections Module - PRD

## Original Problem Statement
Развернуть проект Connections Module с GitHub (https://github.com/svetlanaslinko057/Conectionsv21) в изолированном режиме, следуя документации. Модуль предназначен для справедливого рейтинга инфлюенсеров в социальных сетях.

## Концепция продукта
**Connections Module** — это изолированный модуль платформы для формирования справедливого рейтинга инфлюенсеров в социальных сетях (Twitter и др.).

### Проблема
Традиционные метрики (followers, likes) легко накручиваются и не отражают реальной ценности инфлюенсера.

### Решение
Модуль анализирует:
- **Influence Scoring** — Quality-adjusted score на основе реальных взаимодействий
- **Trend Analysis** — Velocity + Acceleration изменений
- **Early Signal** — Детекция breakout и rising сигналов
- **Risk Detection** — Оценка накрутки и манипуляций
- **Alerts Engine** — Оповещения о важных событиях

## Архитектура

### Tech Stack
- **Backend**: Node.js Fastify (port 8003) + Python FastAPI Proxy (port 8001)
- **Frontend**: React (port 3000)
- **Database**: MongoDB

### Что реализовано (Feb 6, 2026)

#### Backend API (100% работает)
- `/api/health`, `/api/connections/health`, `/api/connections/accounts`
- `/api/connections/score`, `/api/connections/trends`, `/api/connections/early-signal`
- `/api/admin/auth/login`, `/api/admin/connections/overview`, `/api/admin/connections/alerts/*`

#### Frontend Pages (95% работает)
- `/connections` — основной рейтинг
- `/connections/radar` — Early Signal Radar
- `/admin/login` и `/admin/connections` — Admin Panel

## Admin Credentials
```
Username: admin
Password: admin12345
```

## Next Tasks
1. Интеграция Twitter API (если нужны реальные данные)
2. Настройка Telegram Bot для доставки алертов
