# GenAI Credit Card Assistant

A full-stack, AI-powered assistant that handles informational and actionable credit-card queries using a two-agent architecture, RAG, and mock APIs.

---

## Overview

This assistant supports chat and voice inputs and processes two kinds of user queries:

1. Informational Queries
   (e.g., "What is a credit limit?", "How does EMI work?")

2. Actionable Requests
   (e.g., "Block my card", "Convert this transaction to EMI")

The system uses:

* An Intent Classifier Agent for routing
* A Generator Agent powered by Retrieval-Augmented Generation (RAG)
* Mock APIs to simulate realistic credit-card actions

---

## Project Architecture (High-Level)

```
User Interface (Text + Voice)
          |
          v
Intent Classifier Agent
    |                 |
Informational     Actionable
    v                 v
Generator Agent     Mock APIs
      |
      v
RAG Knowledge Base (SentenceTransformers + FAISS)
```

* The Intent Classifier decides whether the query is informational or actionable.
* Informational queries go to the Generator, which uses FAISS vector search + SentenceTransformers to retrieve the most relevant knowledge.
* Actionable queries trigger the appropriate Mock API.
* All responses are returned to the UI.

---

## Project Structure

### backend/ — FastAPI service with AI logic

* main.py – Backend entry point
* assistant.py – Core pipeline
* intent_classifier.py – Intent classification module
* chunker.py – Chunking utility for RAG
* embedder.py – Embedding generator (SentenceTransformers)
* vector_store.py – FAISS-based vector search
* document_loader.py – Loads and processes documents
* generator.py – Generator agent (LLM output)
* mock_api.py – Mock endpoints for actionable tasks
* config.py – API keys & configuration

### frontend/ — React chat interface

* src/ – Components, hooks, context
* public/ – Static assets

---

## Backend Setup

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Add environment variables

Create .env (not included in repo):

```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
EMBED_MODEL_NAME=all-MiniLM-L6-v2
```

### 3. Start backend

```bash
uvicorn backend.main:app --reload
```

---

## Frontend Setup

### 1. Move into frontend directory

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start dev server

```bash
npm start
```

The app runs at: http://localhost:3000

---

## Technologies Used

### Backend

* FastAPI
* Groq API (LLaMA models)
* SentenceTransformers
* FAISS for vector search
* Python

### Frontend

* React.js
* Axios
* Speech-to-text support (optional)

---

## Core Features

### Two-Agent Architecture

* Intent Classifier Agent
* Generator Agent

### RAG Implementation

* Uses SentenceTransformers for embeddings
* Stores vectors in FAISS
* Retrieves relevant chunks for grounding responses

### Action Execution via Mock APIs

Simulates:

* Block card
* Convert to EMI
* Download statement
* Track delivery
* Check balance
* Raise dispute

### Full-Stack Application

* Backend for AI logic
* Frontend for user interactions (chat UI)

---

## Environment Variables (Required)

| Variable           | Description       |
| ------------------ | ----------------- |
| GROQ_API_KEY       | Your Groq API key |
| GROQ_MODEL         | LLM model name    |
| EMBED_MODEL_NAME   | Embedding model   |

---

## How to Use

1. Start backend
2. Start frontend
3. Open browser → localhost:3000
4. Enter:

   * Informational queries → answered via RAG
   * Actionable requests → handled via mock APIs

---
