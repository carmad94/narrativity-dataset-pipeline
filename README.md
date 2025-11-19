# AI Data Ingestion & Enrichment Pipeline

This project implements an end-to-end data pipeline for ingesting, enriching, and visualizing data using Python (FastAPI), Supabase, and React.

## Features
1. Upload Excel/CSV files.
2. Bronze Layer: Store raw data.
3. Silver Layer: Normalize data.
4. Gold Layer: Enrich data using OpenAI API.
5. Story Generation: Generate a narrative from enriched data.
6. React Frontend: Dashboard UI.

## Tech Stack

- Backend: Python, FastAPI
- Frontend: React, Tailwind CSS
- Database: Supabase (PostgreSQL)
- AI Integration: OpenAI API
- Containerization: Docker, Docker Compose

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create `.env` files:
   - Backend (`backend/.env`):
     ```
     SUPABASE_URL=<your-supabase-url>
     SUPABASE_KEY=<your-supabase-key>
     OPENAI_API_KEY=<your-openai-api-key>
     ```
   - Frontend (`frontend/.env`):
     ```
     REACT_APP_API_URL=http://localhost:8000
     ```

3. Run the application:
   ```bash
   docker-compose up --build
   ```

## Usage

- Access the backend API at `http://localhost:8000`.
- Access the React frontend at `http://localhost:3000`.

## Directory Structure

- `backend/`: FastAPI code for data ingestion and processing.
- `frontend/`: React code for the dashboard.
- `docker-compose.yml`: Orchestrates services.

## Testing

You can test endpoints using tools like Postman or cURL.

## Notes

- Ensure your Supabase is set up with the required tables and storage.
- Replace placeholders in `.env` with actual values.