# Connections Module - PRD

## Original Problem Statement
1. Развернуть проект Connections Module с GitHub
2. Сделать Connections как dropdown в sidebar (как Sentiment) с 2 под-вкладками:
   - **Influencers** - таблица аккаунтов
   - **Graph** - граф связей между инфлюенсерами

## Архитектура

### Navigation Structure
```
Sidebar:
├── ...
├── Sentiment (dropdown)
│   ├── Analyzer
│   ├── Twitter Feed
│   └── Twitter AI
├── Dashboard
└── Connections (dropdown)  ← НОВОЕ
    ├── Influencers → /connections
    └── Graph → /connections/graph
```

### Tech Stack
- **Backend**: Node.js Fastify (8003) + Python FastAPI Proxy (8001)
- **Frontend**: React (3000) с ForceGraphCore
- **Database**: MongoDB

## Что реализовано (Feb 6, 2026)

### Sidebar Navigation
- ✅ Connections как dropdown (как Sentiment)
- ✅ Influencers и Graph под-вкладки
- ✅ Connections по умолчанию раскрыт

### Influencers Page (/connections)
- ✅ Таблица аккаунтов с Influence Score, Risk, Followers
- ✅ Поиск и фильтры
- ✅ Compare функционал
- ✅ Tabs: Influencers (активный) | Graph

### Graph Page (/connections/graph)
- ✅ ForceGraphCore визуализация (тот же что в Graph Intelligence → Routes)
- ✅ 30 nodes, 430+ edges
- ✅ Tabs: Influencers | Graph (активный)
- ✅ Refresh кнопка
- ✅ Legend с цветовой кодировкой

### Backend API
- GET /api/connections/graph - полный граф
- POST /api/connections/graph - граф с фильтрами
- GET /api/connections/graph/ranking - ранкинг
- GET /api/connections/graph/node/:id - детали узла

## Тестирование
- Frontend: 100%
- Backend: 83%

## MOCK данные
Граф работает на расчётных данных (generateMockAccounts). Twitter API не подключен.

## Next Tasks
1. Интеграция Twitter API для реальных audience overlaps
2. Улучшить Compare функционал
3. Добавить фильтры в Graph page
