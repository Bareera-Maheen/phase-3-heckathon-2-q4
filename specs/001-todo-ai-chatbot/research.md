# Research: Phase III Todo AI Chatbot

## Decision: OpenAI Agents SDK & MCP Integration
- **Selection**: Use OpenAI Agents SDK for the conversational logic and the Official MCP SDK for tool execution.
- **Rationale**: This combination aligns with the project constitution's requirement for decoupled AI logic and tool-based system interaction.
- **Alternatives Considered**: 
    - LangChain: Rejected due to higher complexity and overhead compared to the streamlined Agents SDK.
    - Custom Function Calling: Rejected as MCP provides a more standardized and extensible interface for tools.

## Decision: Stateless Context Reconstruction
- **Selection**: On every request to `/api/{user_id}/chat`, fetch the last N messages from the `Message` table for the given `conversation_id`.
- **Rationale**: Ensures the backend remains strictly stateless as per principle I, while maintaining continuity (principle II).
- **Alternatives Considered**:
    - Redis Caching: Rejected to avoid adding another dependency and to keep the source of truth in the primary database.

## Decision: MCP Server Architecture
- **Selection**: Implement a standalone MCP server module within the backend that exposes `add_task`, `list_tasks`, `complete_task`, `delete_task`, and `update_task`.
- **Rationale**: Complies with principle IV. Tools receive `user_id` to ensure user-scoping (principle VI).
- **Alternatives Considered**:
    - Direct Database Access in Agent: Rejected as it violates principle III.

## Decision: Frontend Chat Interface
- **Selection**: OpenAI ChatKit integrated into the Next.js frontend.
- **Rationale**: Provides a modern, optimized chat UI with minimal custom business logic, adhering to principle V.
- **Alternatives Considered**:
    - Custom React Chat UI: Rejected to minimize development effort and focus on the backend AI integration.
