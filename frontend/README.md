```markdown
# Dataset Dashboard (React)

A small React dashboard to upload datasets and view AI-enriched ("Gold") records.

Features:
- Upload dataset (file upload to backend `/upload` endpoint)
- List uploaded (bronze) records (GET `/bronze`)
- View AI-enriched data for an ID (GET `/gold/:id`, fallback to `/generate-story/:id`)

Assumptions:
- Your backend exposes:
  - POST /upload (multipart/form-data) — accepts a file and returns info about saved bronze records
  - GET /bronze — returns a list of uploaded raw records (each with `id` or `hash`)
  - GET /gold/:id — returns enriched gold data for a given id
  - fallback: GET /generate-story/:id returns a narrative for the id

If your endpoints are different, set REACT_APP_API_URL in `.env` and update src/api.js accordingly.

Quick start
1. Copy files into a directory created with Create React App or use this structure.
2. Create `.env` (see `.env.example`) and set REACT_APP_API_URL to your backend URL (e.g., http://localhost:8000)
3. Install:
```bash
npm install
```
4. Run:
```bash
npm start
```

Environment variables
- REACT_APP_API_URL — Base URL of your backend API (default: http://localhost:8000)

Notes & tips
- The upload form posts a file as `file` field in multipart/form-data. Ensure your backend accepts that.
- The dataset list expects the bronze endpoint to return JSON array or an object containing an array at `.records`.
- The Gold viewer tries GET /gold/:id, then /generate-story/:id, then /gold?id=... — adjust logic as needed.
- Add authentication (Supabase or other) as needed. For Supabase, you can include Authorization headers in `src/api.js` using your anon/service key (store it securely).

Handling CORS
- Ensure your backend allows requests from the origin running the React app (Access-Control-Allow-Origin).

```