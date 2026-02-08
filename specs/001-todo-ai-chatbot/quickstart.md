# Quickstart: Phase III Todo AI Chatbot

## Setup Environment

### Backend
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure `.env`:
   ```env
   DATABASE_URL=postgresql://...
   OPENAI_API_KEY=sk-...
   BETTER_AUTH_SECRET=...
   ```
4. Run migrations: `python -m src.models.migrations`.
5. Start server: `uvicorn src.api.main:app --reload`.

### Frontend
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Configure `.env.local`:
   ```env
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   NEXT_PUBLIC_OPENAI_CHATKIT_ID=...
   ```
4. Start development server: `npm run dev`.

## Verification Steps

1. **Authentication**: Sign in via the Better Auth UI.
2. **Chat**: Open the chat interface.
3. **Task Creation**: Type "Add a task to prepare the demo for tomorrow".
4. **Task Listing**: Type "What are my tasks?".
5. **Statelessness Check**: Refresh the page or restart the backend server; previous messages should still be visible and context maintained.
