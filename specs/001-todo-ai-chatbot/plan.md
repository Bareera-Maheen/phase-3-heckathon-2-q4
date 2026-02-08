# Implementation Plan: Phase III Todo AI Chatbot

**Branch**: `001-todo-ai-chatbot` | **Date**: 2026-02-08 | **Spec**: [specs/001-todo-ai-chatbot/spec.md](specs/001-todo-ai-chatbot/spec.md)
**Input**: Feature specification from `/specs/001-todo-ai-chatbot/spec.md`

## Summary

The goal is to implement a conversational AI interface for the existing Todo application. The technical approach involves a FastAPI backend that uses the OpenAI Agents SDK for conversational logic and the Official MCP SDK for task-related operations. The system is strictly stateless, reconstructing conversation history from a PostgreSQL database (Neon) for every request. The frontend uses OpenAI ChatKit for a seamless chat experience, and Better Auth handles user authentication and scoping.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript/Next.js 14+
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, OpenAI ChatKit, Better Auth, SQLModel
**Storage**: Neon Serverless Postgres
**Testing**: pytest (backend), Vitest/Playwright (frontend)
**Target Platform**: Vercel (Frontend), Railway/Render (Backend), Neon (Database)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: < 3s response time for chat interactions (excluding AI latency)
**Constraints**: Stateless server architecture, strict user-scoped data access, MCP-only task modifications
**Scale/Scope**: Conversational CRUD for personal todos, multi-turn conversation support

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Stateless Server Architecture**: ✅ The plan reconstructs history from DB every request.
- **Persistent Conversation Continuity**: ✅ `Conversation` and `Message` tables defined for persistence.
- **MCP-Driven AI Logic**: ✅ AI Agent uses MCP tools exclusively for task operations.
- **Official MCP SDK & Stateless Tools**: ✅ MCP server will use the official SDK with stateless handlers.
- **Decoupled Frontend (OpenAI ChatKit)**: ✅ Frontend logic limited to chat UI and backend communication.
- **Secure User Scoping (Better Auth)**: ✅ All requests and data access scoped by `user_id`.
- **Agentic Dev Stack Workflow**: ✅ Following Spec -> Plan -> Tasks -> Implementation sequence.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-ai-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/             # FastAPI endpoints (chat)
│   ├── agents/          # OpenAI Agents logic
│   ├── mcp/             # MCP Server implementation
│   ├── models/          # SQLModel entities (Task, Conversation, Message)
│   └── services/        # Database and auth services
└── tests/
    ├── integration/
    └── unit/

frontend/
├── app/                 # Next.js App Router (ChatKit integration)
├── components/          # Chat UI components
├── services/            # API client for backend chat
└── tests/
```

**Structure Decision**: Option 2: Web application (frontend + backend)

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
