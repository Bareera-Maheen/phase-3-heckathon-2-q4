# Feature Specification: Phase III Todo AI Chatbot

**Feature Branch**: `001-todo-ai-chatbot`  
**Created**: 2026-02-08  
**Status**: Draft  
**Input**: User description: "Produce a complete technical specification for Phase III Todo AI Chatbot in strict compliance with the defined constitution. The system shall provide a conversational interface that allows authenticated users to manage todo tasks using natural language. Users shall be able to add new tasks, list tasks with filters, update task details, mark tasks as completed, and delete tasks through conversational commands. The frontend shall be built using OpenAI ChatKit and shall communicate with the backend via a single HTTP endpoint. The frontend shall support hosted deployment and must comply with OpenAI domain allowlist requirements. The frontend shall pass user messages and conversation identifiers to the backend and render assistant responses. The backend shall be implemented using Python FastAPI and shall expose a POST endpoint at /api/{user_id}/chat. This endpoint shall accept a user message and an optional conversation_id. If no conversation_id is provided, a new conversation shall be created. Upon receiving a request, the backend shall retrieve the full conversation history from the database, append the new user message, and construct a message array for the AI agent. The backend shall persist the user message before invoking the agent. The AI agent shall be implemented using the OpenAI Agents SDK. The agent shall interpret the user’s natural language input and determine whether to invoke one or more MCP tools. The agent shall follow explicit behavior rules for task creation, listing, updating, completion, and deletion. The MCP server shall be implemented using the Official MCP SDK and shall expose tools named add_task, list_tasks, complete_task, delete_task, and update_task. Each tool shall accept user_id as a required parameter and shall interact with the database using SQLModel. Each tool shall return structured output as defined in the requirements. The database shall be Neon Serverless PostgreSQL and shall contain tables for Task, Conversation, and Message. All records shall be scoped by user_id. Timestamps shall be recorded for auditing and ordering. The backend shall store the assistant’s response and any tool invocations in the database and return the response to the client. The system shall gracefully handle errors and provide friendly confirmations for successful actions. The system must support conversational continuity."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Task Management (Priority: P1)

As an authenticated user, I want to manage my todo tasks using natural language so that I can interact with the system efficiently and intuitively.

**Why this priority**: This is the core functionality of the Phase III update.

**Independent Test**: A user sends a message "Add a task to buy milk tomorrow" and the assistant confirms the task creation.

**Acceptance Scenarios**:

1. **Given** an authenticated session, **When** the user sends "Remind me to call John at 5pm", **Then** the assistant confirms the task "call John" is added with a 5pm deadline.
2. **Given** an existing task "buy milk", **When** the user sends "I bought the milk", **Then** the assistant marks the "buy milk" task as completed and confirms it.

---

### User Story 2 - Task Listing and Filtering (Priority: P2)

As an authenticated user, I want to list and filter my tasks through natural language so that I can easily see what I need to do.

**Why this priority**: Essential for managing a list of tasks over time.

**Independent Test**: A user sends "Show me my pending tasks" and the assistant lists all tasks that are not completed.

**Acceptance Scenarios**:

1. **Given** multiple tasks (some completed, some pending), **When** the user sends "List my incomplete tasks", **Then** only the pending tasks are displayed.
2. **Given** a task list, **When** the user sends "What's on my list for today?", **Then** the assistant lists tasks due today.

---

### User Story 3 - Conversational Continuity (Priority: P3)

As an authenticated user, I want the assistant to remember our previous messages so that I can have a natural, multi-turn conversation.

**Why this priority**: Enhances the AI experience and allows for clarifications or follow-up commands.

**Independent Test**: A user adds a task and then asks "What did I just add?", and the assistant correctly identifies the task.

**Acceptance Scenarios**:

1. **Given** a previous message about a task, **When** the user asks a follow-up question like "Change its priority to high", **Then** the assistant correctly identifies "it" as the previously mentioned task and updates it.

---

### Edge Cases

- **Ambiguous Commands**: If the user says "Delete it" without context, the assistant MUST ask for clarification.
- **Unauthorized Access**: If a user attempts to access another user's conversation_id, the system MUST return an error.
- **Empty Commands**: If the user sends an empty message, the system MUST respond with a prompt to help the user get started.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a natural language conversational interface using OpenAI ChatKit.
- **FR-002**: System MUST allow users to add, list, update, complete, and delete tasks via conversational commands.
- **FR-003**: System MUST expose a single chat endpoint at `/api/{user_id}/chat`.
- **FR-004**: System MUST reconstruct conversation history from the database for every request to ensure statelessness.
- **FR-005**: AI Agent MUST use MCP tools to interact with the database.
- **FR-006**: All data access (tasks, conversations, messages) MUST be scoped to the authenticated `user_id`.
- **FR-007**: System MUST persist all user and assistant messages in a `Message` table.
- **FR-008**: System MUST support multiple conversations per user via `conversation_id`.

### Key Entities

- **Task**: Represents a todo item. Attributes: ID, title, status (pending/completed), deadline, priority, user_id.
- **Conversation**: Represents a chat session. Attributes: ID, user_id, created_at.
- **Message**: Represents a single exchange in a conversation. Attributes: ID, conversation_id, role (user/assistant), content, created_at.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a task via natural language with a response time under 3 seconds (excluding AI generation time).
- **SC-002**: 90% of standard task management commands (add, list, delete) are correctly mapped to MCP tools.
- **SC-003**: 100% of data is correctly scoped to the `user_id`, with no data leakage between users.
- **SC-004**: System successfully reloads and applies conversation history for at least the last 10 messages in every turn.
