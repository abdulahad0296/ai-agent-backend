# Full stack AI Agent with Asynchronous Task Queue

> A production-ready, Dockerized AI Agent capable of real-time web search (RAG) and persistent conversational memory. Built with Django, Celery, Redis and Llama 3 (Groq)

## Overview

This project implements a scalable **Event-Driven Architecture** to handle high latency AI tasks. Unlike simple API wrappers, this application decouples the AI inference from the web server using an asynchronous worker pattern. This ensures UI remains responsive while the agent performs complex reasoning and web searching in the background.

**Key Capabilities:**

* **Context Awareness:** Remembers previous turns in the convo (e.g., "Who is Elon Musk?" -> "How old is *he*?").
* **RAG (Real-Time Search):** Uses DuckDuckGo to fetch live data for queries about current events (e.g., "Stock price of Apple", "Sports scores").
* **Async Processing:** Offloads heavy LLM & Search operations to Celery workers backed by Redis.
* **Multi-User Privacy:** Secure session management ensures users cannot see each other's chats.

---

## Tech Stack

* **Backend:** Python 3.13, Django 6.0
* **Task Queue:** Celery (Distributed Task Queue)
* **Message Broker:** Redis
* **LLM Provider:** Groq API (Llama-3-8b-8192)
* **Search Tool:** DuckDuckGo Search (DDGS)
* **Containerization:** Docker & Docker Compose
* **Database:** SQLite (Dev) / PostgreSQL (Ready for Prod)

---

## Architecture

1.  **User Request:** The Django View receives a prompt via AJAX.
2.  **Session Check:** The app verifies the User Session and Conversation ID.
3.  **Task Dispatch:** The prompt is sent to the **Redis Queue**. The View returns a `task_id` immediately.
4.  **Worker Processing:** A **Celery Worker** picks up the task:
    * Retrieves conversation history from the DB.
    * Performs a Web Search (if needed).
    * Constructs a context-rich prompt for the LLM.
5.  **Result Polling:** The frontend polls the backend until the worker marks the task as `SUCCESS`.

---

## Quick Start (Docker)

The easiest way to run this app is with Docker Compose.

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* [Git](https://git-scm.com/) installed. 

### Step 1: Clone the Repo

### Step 2: Configure the environment

Create a .env file in the root directory
```bash
# .env
GROQ_API_KEY=gsk_your_actual_api_key_here
DJANGO_SECRET_KEY=any_random_string
DEBUG=True
REDIS_URL=redis://redis:6379/0
```

### Step 3: Build and run

```bash
docker-compose up --build
```

The app will be available at: http://localhost:8000/agents/


## Testing the Agent

### 1. Memory Test:

* User: "Who is the CEO of Tesla?"
* AI: "Elon Musk..."
* User: "How old is he?" (Tests context retention)

### 2. Privacy Test:

* Open the chat in an Incognito window. You will see a fresh empty chat, proving data isolation.

## License
### MIT License. Free to use and modify.