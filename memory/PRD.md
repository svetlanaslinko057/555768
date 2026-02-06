# Connections Module - PRD

## Original Problem Statement
Развернуть Connections Module с GitHub и реализовать полную навигационную структуру:
- Connections как dropdown в sidebar (как Sentiment)
- 3 под-вкладки: **Influencers**, **Graph**, **Radar**
- Graph с полной логикой фильтров из первой итерации

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
└── Connections (dropdown)  ← РЕАЛИЗОВАНО
    ├── Influencers → /connections
    ├── Graph → /connections/graph
    └── Radar → /connections/radar
```

### Tech Stack
- **Backend**: Node.js Fastify (8003) + Python FastAPI Proxy (8001)
- **Frontend**: React (3000) с ForceGraphCore
- **Database**: MongoDB

## Что реализовано (Feb 6, 2026)

### Sidebar Navigation
- ✅ Connections как dropdown (как Sentiment)
- ✅ 3 под-вкладки: Influencers, Graph, Radar
- ✅ Connections по умолчанию раскрыт

### Influencers Page (/connections)
- ✅ Навигационные табы: Influencers | Graph | Radar
- ✅ Таблица аккаунтов с Influence Score, Risk, Followers
- ✅ Поиск и фильтры
- ✅ Compare функционал

### Graph Page (/connections/graph)
- ✅ **ForceGraphCore** визуализация (30 nodes, 435 edges)
- ✅ **Filter Panel**:
  - NODES: Profile (Retail/Influencer/Whale), Early Signal (Breakout/Rising/None), Risk Level (Low/Medium/High)
  - EDGES: Strength (Low/Medium/High)
  - VIEW: Hide isolated nodes, Max nodes slider
- ✅ **Ranking Sidebar**: сортировка по Influence/Signal
- ✅ **Node Details Panel**: Influence Score, Early Signal, Risk, Trend, Connected nodes, Why Connected
- ✅ **Legend** с цветовой кодировкой

### Radar Page (/connections/radar)
- ✅ Навигационные табы: Influencers | Graph | Radar
- ✅ Scatter plot с Alpha Zone
- ✅ Фильтры по Profile и Signal
- ✅ Compare Mode
- ✅ Radar/Table view toggle

## Backend API
- GET/POST /api/connections/graph - граф с фильтрами
- GET /api/connections/graph/ranking - ранкинг
- GET /api/connections/graph/node/:id - детали узла

## Тестирование
- Frontend: **100%**
- Navigation: **100%**
- Visualization: **100%**
- Interaction: **100%**

## MOCK данные
Граф работает на расчётных данных (generateMockAccounts). Twitter API не подключен.

## Next Tasks
1. Интеграция Twitter API для реальных overlaps
2. Cluster detection для группировки связанных инфлюенсеров
3. Дополнительные layouts (radial, clustered)
