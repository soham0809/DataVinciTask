## Grippi Campaign Analytics Dashboard (Simplified)

This is a very small full‑stack app that shows a list of marketing campaigns in a table with a simple status filter.

- **Frontend**: Next.js (React, Typescript) with plain CSS  
- **Backend**: FastAPI (Python) with SQLite  
- **Database script**: `database.sql` (works for PostgreSQL or SQLite)

---

## 1. Project Structure

- **frontend** – Next.js app (table UI and filter)
- **backend** – FastAPI app (`/campaigns` endpoint)
- **database.sql** – SQL to create and seed the `campaigns` table

---

## 2. Backend (FastAPI)

### 2.1. Install and run locally

From the project root:

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # on Windows
pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- `http://localhost:8000/campaigns`
- Docs: `http://localhost:8000/docs`

The first time the server runs it will create `campaigns.db` (SQLite) and insert 10 sample campaigns.

### 2.2. Deploying backend to Railway (outline)

1. Push this repo to GitHub.  
2. On Railway, create a new project from this repo and select the `backend` folder.  
3. Use the default Python environment, set the start command to:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. Deploy and note the public URL, e.g. `https://your-railway-app.up.railway.app`.

---

## 3. Database SQL (PostgreSQL / SQLite)

The `database.sql` file creates the `campaigns` table and inserts 10 sample rows.

### 3.1. Example commands

**SQLite (local quick test):**

```bash
sqlite3 campaigns.db < ../database.sql
```

**PostgreSQL:**

```bash
psql -h HOST -U USER -d DB_NAME -f database.sql
```

You can then run:

```sql
SELECT * FROM campaigns WHERE status = 'Active';
```

---

## 4. Frontend (Next.js)

### 4.1. Install and run locally

From the project root:

```bash
cd frontend
npm install
npm run dev
```

The app will run on `http://localhost:3000`.

By default the frontend calls:

```text
http://localhost:8000/campaigns
```

Make sure the FastAPI backend is running on port 8000 when you test locally.

### 4.2. Configure API URL (for deployment)

Set the environment variable `NEXT_PUBLIC_API_BASE_URL`:

- **Local (optional)**: create `.env.local` in `frontend`:

  ```text
  NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
  ```

- **Production (Vercel)**: in Vercel project settings, add  
  `NEXT_PUBLIC_API_BASE_URL=https://your-railway-app.up.railway.app`

### 4.3. Deploying frontend to Vercel (outline)

1. Push the repo to GitHub.  
2. On Vercel, "Import Project" from GitHub.  
3. Set the root directory to `frontend`.  
4. Add `NEXT_PUBLIC_API_BASE_URL` environment variable pointing to your Railway backend.  
5. Deploy – Vercel will give you a public URL for the dashboard.

---

## 5. What the UI Does

- Shows a table with columns: **Campaign Name**, **Status**, **Clicks**, **Cost**, **Impressions**.
- Fetches data from `GET /campaigns` on page load.
- Simple dropdown filter:
  - **All**
  - **Active**
  - **Paused**
- Basic loading and error message states.

---

## 6. For the Loom Video

When recording your Loom video, you can:

- Walk through the folder structure (`frontend`, `backend`, `database.sql`).  
- Explain `backend/main.py`:
  - Database model (`CampaignModel`)
  - Pydantic schema (`Campaign`)
  - Seed function (inserts 10 rows)
  - `/campaigns` route that reads from the DB.  
- Explain `frontend/pages/index.tsx`:
  - React state for campaigns, filter, loading, and error
  - `useEffect` that fetches from the backend
  - Filtered list and table rendering.



