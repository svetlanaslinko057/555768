# Connections Module - PRD

## Original Problem Statement
Развернуть проект Connections Module с GitHub и реализовать Connections Graph - визуализацию графа влияния между инфлюенсерами.

## Концепция продукта
**Connections Module** — изолированный модуль для справедливого рейтинга инфлюенсеров в социальных сетях.

## Архитектура

### Tech Stack
- **Backend**: Node.js Fastify (port 8003) + Python FastAPI Proxy (port 8001)
- **Frontend**: React (port 3000) с ForceGraphCore (react-force-graph-2d)
- **Database**: MongoDB

### Структура Connections
```
/connections
├── Influencers     - таблица рейтинга аккаунтов
├── Radar           - Early Signal scatter plot
└── Graph           - граф связей (НОВАЯ ВКЛАДКА)
```

## Что реализовано (Feb 6, 2026)

### Connections Graph (NEW)
**Backend API:**
- `GET /api/connections/graph` - полный граф (30 nodes, 435 edges)
- `POST /api/connections/graph` - граф с фильтрами
- `GET /api/connections/graph/ranking` - ранкинг для sidebar
- `GET /api/connections/graph/node/:id` - детали узла

**Frontend:**
- ForceGraphCore визуализация с drag/zoom/pan
- Filter Panel (Profile, Early Signal, Risk, Edge Strength)
- Ranking Sidebar с сортировкой по Influence/Signal
- Node Details Panel при клике
- Legend с цветовой кодировкой

### Существующий функционал
- `/connections` - таблица инфлюенсеров с рейтингами
- `/connections/radar` - Early Signal Radar
- `/admin/connections` - Admin Control Plane

## Тестирование
- Backend: 100% (15/15 tests)
- Frontend: 95% (11/12 features)

## Admin Credentials
```
Username: admin
Password: admin12345
```

## P0/P1/P2 Features

### ✅ P0 (Завершено)
- [x] Connections Graph как под-вкладка
- [x] Mock data generation (30 nodes, 435 edges)
- [x] Фильтрация по всем параметрам
- [x] Ranking sidebar

### 🔜 P1 (Next)
- [ ] Twitter Integration (реальные данные)
- [ ] Node click → полный профиль
- [ ] Edge hover → explain relationship

### P2 (Backlog)
- [ ] Telegram/Discord alert delivery
- [ ] Export graph as image
- [ ] Custom filter presets

## Next Tasks
1. Интеграция Twitter API для реальных overlaps
2. Добавить cluster detection algorithm
3. Реализовать graph layouts (radial, clustered)
