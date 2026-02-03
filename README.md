# Real-Time Trading Notification System

Scalable real-time system that sends new deal updates to users who follow one or more company tags/symbols.

### What it does

- Merchants post new deals via API
- Users receive only deals for the tags they follow
- Updates arrive via WebSocket in < 1 second (usually 100–300 ms)

### Core design choices

- **One Redis Pub/Sub channel** ("new_deals")
  → every app server subscribes only once
  → avoids thousands of connections per user

- **Server-side fan-out**
  → app servers receive every deal → filter locally → send only to relevant connected users
  → no per-tag channels, no client-side filtering

- **Per-user batching** (default 100 ms)
  → messages are collected briefly → sent as JSON array
  → fewer packets, better mobile experience, less server overhead

- **In-memory tracking** per app instance
  tag → connected WebSockets
  WebSocket → subscribed tags
  → very fast, scales horizontally by adding more app servers

### Tech stack (2025–2026 style)

- FastAPI                (REST + WebSocket)
- SQLModel               (database models)
- PostgreSQL / SQLite    (persistent data)
- Redis Pub/Sub          (lightweight broadcast)
- asyncio + in-memory dicts   (fan-out & batching)

### Why these choices?

- **Redis single channel** → constant low connection count
- **No Kafka / RabbitMQ** → overkill, higher latency & ops cost
- **In-memory fan-out** → fastest possible delivery (no extra network hops)
- **Batching** → huge win for throughput and battery/network efficiency
- **FastAPI + SQLModel** → modern, async, type-safe, easy to maintain

### Quick start

```bash
poetry install
uvicorn src.main:app --reload
