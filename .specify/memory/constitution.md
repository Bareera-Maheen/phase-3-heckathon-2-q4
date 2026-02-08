# Phase III Todo AI Chatbot Constitution

<!--
  This constitution defines the immutable rules and architectural constraints 
  for the Phase III Todo AI Chatbot project.
-->

## Core Principles

### I. Stateless Server Architecture
The FastAPI backend must be strictly stateless. It must not store any conversation state, session 
data, agent memory, or application state in memory between requests. Every request must be 
handled independently and must reconstruct all required context from the database.

### II. Persistent Conversation Continuity
All conversation continuity must be achieved through persistent storage. Conversations must be 
stored in a `Conversation` table, and every message exchanged must be stored in a `Message` 
table. The server must reload the entire conversation history from the database on each request 
to provide context to the AI agent.

### III. MCP-Driven AI Logic
The AI logic must be implemented using the OpenAI Agents SDK. The AI agent is prohibited from 
accessing the database or application services directly. All task-related operations must be 
performed exclusively through MCP tools exposed by an MCP server.

### IV. Official MCP SDK & Stateless Tools
The MCP server must be implemented using the Official MCP SDK. It must expose standardized tools 
for task CRUD operations. Each MCP tool must be stateless and must receive all required inputs 
explicitly, including the authenticated user identifier. MCP tools are the only components 
permitted to modify task data.

### V. Decoupled Frontend (OpenAI ChatKit)
The frontend must be implemented using OpenAI ChatKit. Its sole responsibility is to provide a 
conversational user interface and communicate with the backend chat endpoint. It must not contain 
any business logic or task-specific logic.

### VI. Secure User Scoping (Better Auth)
Authentication must be enforced using Better Auth. Every request must be associated with a 
`user_id`, and all data access (tasks, conversations, messages) must be strictly scoped to that 
user. No cross-user data access is permitted under any circumstances.

### VII. Agentic Dev Stack Workflow
All development must follow the Agentic Dev Stack workflow in strict order: Specification, 
Planning, Task Decomposition, and Implementation. Manual coding outside of generated artifacts 
or outside this sequence is strictly prohibited.

## Technology Stack

- **Backend**: FastAPI (Python)
- **AI Orchestration**: OpenAI Agents SDK
- **Tooling**: Official MCP SDK (Server/Client)
- **Frontend**: Next.js (TypeScript) with OpenAI ChatKit
- **Authentication**: Better Auth
- **Database**: Neon Serverless Postgres (via SQLAlchemy)
- **Workflow**: Claude Code + Spec-Kit Plus

## Development Workflow

1. **Specification**: Define user stories, requirements, and success criteria in `spec.md`.
2. **Planning**: Technical research, data modeling, and architectural decisions in `plan.md`.
3. **Task Decomposition**: Break down implementation into granular, testable tasks in `tasks.md`.
4. **Implementation**: Execute tasks using agentic tools. All code must align with the `plan.md`.

## Governance
This constitution supersedes all other practices and documentation. Any architectural or design 
decision that violates these principles must be rejected. Amendments to this constitution 
require a version bump and explicit documentation of the rationale.

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08