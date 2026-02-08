---
id: 001
title: Initialize Project Constitution
stage: constitution
date: 2026-02-08
surface: agent
model: gemini-2.0-flash-thinking-exp
feature: none
branch: main
user: baree
command: /sp.constitution
labels: [constitution, setup, mcp, stateless]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution You are an autonomous senior software architect operating under the Spec-Kit Plus framework. Your responsibility is to define the immutable constitution for a project titled “Phase III Todo AI Chatbot”.

The purpose of this system is to extend an existing todo application by introducing an AI-powered conversational interface that allows users to manage todo tasks using natural language. The system must be built using MCP server architecture and must use Claude Code and Spec-Kit Plus as part of an Agentic Dev Stack workflow.

The system must strictly follow a stateless server architecture. The FastAPI backend must not store any conversation state, session data, agent memory, or application state in memory between requests. Every request must be handled independently and must reconstruct all required context from the database.

All conversation continuity must be achieved through persistent storage. Conversations must be stored in a Conversation table, and every message exchanged between the user and the assistant must be stored in a Message table. The server must reload the entire conversation history from the database on each request.

The AI logic must be implemented using the OpenAI Agents SDK. The AI agent must not access the database or application services directly. All task-related operations must be performed exclusively through MCP tools exposed by an MCP server implemented using the Official MCP SDK.

The MCP server must expose standardized tools for task creation, listing, updating, completion, and deletion. Each MCP tool must be stateless and must receive all required inputs explicitly, including the authenticated user identifier. MCP tools are the only components permitted to modify task data in the database.

The frontend must be implemented using OpenAI ChatKit. Its sole responsibility is to provide a conversational user interface and communicate with the backend chat endpoint. It must not contain business logic or task logic.

Authentication must be enforced using Better Auth. Every request must be associated with a user_id, and all data access must be scoped to that user. No cross-user data access is permitted.

All development must follow the Agentic Dev Stack workflow in the order: specification, planning, task decomposition, and implementation. Manual coding outside generated artifacts is not allowed.

This constitution is binding and must govern all architectural, design, and implementation decisions without exception.

## Response snapshot

Updated the project constitution at `.specify/memory/constitution.md` with core principles for statelessness, persistent continuity, MCP-driven AI logic, and strict agentic workflows.

## Outcome

- ✅ Impact: Established the architectural bedrock for the AI Chatbot project.
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify for feature definition.
- 🧠 Reflection: The principles are strict, ensuring high maintainability and scalability through statelessness and clear tool-based separation of concerns.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
