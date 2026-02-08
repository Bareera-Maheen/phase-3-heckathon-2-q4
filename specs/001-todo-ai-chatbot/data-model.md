# Data Model: Phase III Todo AI Chatbot

## Entities

### Task
Represents a todo item managed by the user.
- **id**: `UUID` (Primary Key)
- **title**: `String` (Required)
- **description**: `String` (Optional)
- **status**: `Enum` (pending, completed)
- **deadline**: `DateTime` (Optional)
- **priority**: `Enum` (low, medium, high)
- **user_id**: `String` (Required, Indexed) - Owner of the task.
- **created_at**: `DateTime`
- **updated_at**: `DateTime`

### Conversation
Represents a chat session between a user and the AI assistant.
- **id**: `UUID` (Primary Key)
- **user_id**: `String` (Required, Indexed) - Owner of the conversation.
- **title**: `String` (Optional, generated from first message)
- **created_at**: `DateTime`

### Message
Represents an individual exchange within a conversation.
- **id**: `UUID` (Primary Key)
- **conversation_id**: `UUID` (Foreign Key -> Conversation.id)
- **role**: `Enum` (user, assistant, tool, system)
- **content**: `Text` (Required)
- **tool_calls**: `JSON` (Optional, for recording tool usage)
- **user_id**: `String` (Required, Indexed) - Redundant for performance, ensuring strict scoping.
- **created_at**: `DateTime`

## Relationships
- **Conversation** has many **Messages**.
- **User** has many **Conversations**.
- **User** has many **Tasks**.

## Validation Rules
- `user_id` must be present on all entities.
- `Task.title` cannot be empty.
- `Message.role` must be one of the defined roles.
- All timestamps must be in UTC.
