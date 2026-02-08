# Tasks: Phase III Todo AI Chatbot

**Input**: Design documents from `/specs/001-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (backend/, frontend/) per implementation plan
- [x] T002 Initialize Python project in backend/ and install dependencies (FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK)
- [x] T003 Initialize Next.js project in frontend/ and install dependencies (OpenAI ChatKit, Better Auth)
- [x] T004 [P] Configure linting and formatting tools (ruff for backend, prettier for frontend)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Setup Neon Database connection and SQLModel engine in backend/src/database.py
- [x] T006 [P] Implement SQLModel entities (Task, Conversation, Message) in backend/src/models/entities.py
- [x] T007 [P] Configure Better Auth on frontend and backend for secure user scoping
- [x] T008 Setup basic FastAPI app with chat endpoint skeleton in backend/src/api/main.py
- [x] T009 Initialize MCP Server using Official SDK in backend/src/mcp/server.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Manage tasks (add/update/complete/delete) using natural language commands.

**Independent Test**: Send "Add a task to buy milk tomorrow" and verify the task is created in the database and a confirmation is received.

### Implementation for User Story 1

- [x] T010 [P] [US1] Implement MCP `add_task` tool with SQLModel in backend/src/mcp/tools.py
- [x] T011 [P] [US1] Implement MCP `update_task` and `complete_task` tools in backend/src/mcp/tools.py
- [x] T012 [P] [US1] Implement MCP `delete_task` tool in backend/src/mcp/tools.py
- [x] T013 [US1] Define AI Agent system prompt and register MCP tools using OpenAI Agents SDK in backend/src/agents/todo_agent.py
- [x] T014 [US1] Implement chat logic: persist user message, execute agent with tools, persist assistant response in backend/src/api/chat.py
- [x] T015 [US1] Integrate OpenAI ChatKit in frontend/app/page.tsx and connect to the /api/{user_id}/chat backend endpoint

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Task Listing and Filtering (Priority: P2)

**Goal**: List and filter tasks using natural language queries.

**Independent Test**: Send "Show me my pending high priority tasks" and verify the correct filtered list is returned.

### Implementation for User Story 2

- [x] T016 [P] [US2] Implement MCP `list_tasks` tool with filtering support (status, priority, deadline) in backend/src/mcp/tools.py
- [x] T017 [US2] Update AI Agent system prompt to handle complex listing and filtering queries in backend/src/agents/todo_agent.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Conversational Continuity (Priority: P3)

**Goal**: Maintain multi-turn conversation context by reloading history from the database.

**Independent Test**: Add a task, then ask "What did I just add?", and verify the assistant correctly identifies the task based on history.

### Implementation for User Story 3

- [x] T018 [US3] Implement conversation history reconstruction service in backend/src/services/history.py
- [x] T019 [US3] Update chat endpoint to fetch history and pass it as a message array to the AI Agent in backend/src/api/chat.py

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T020 [P] Implement comprehensive error handling and user-friendly failure messages in backend/src/utils/errors.py
- [x] T021 [P] Finalize environment variable configuration and deployment settings in backend/.env and frontend/.env.local
- [x] T022 Run quickstart.md validation and perform final end-to-end user journey testing

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1 completion. BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Phase 2 completion.
  - US1 (P1) is the MVP and should be prioritized.
  - US2 and US3 can proceed in parallel or sequentially after US1.
- **Polish (Final Phase)**: Depends on all user stories being complete.

### Implementation Strategy

1. **MVP First**: Complete Phase 1, 2, and 3 to deliver a functional natural language todo manager.
2. **Incremental Delivery**: Add Phase 4 (Listing) and Phase 5 (Continuity) as follow-up increments.
3. **Continuous Validation**: Test each story independently upon completion using the defined "Independent Test" criteria.