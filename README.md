## Grippi Campaign Analytics Dashboard (Simplified)

This is a very small full‑stack app that shows a list of marketing campaigns in a table with a simple status filter.

- **Frontend**: Next.js (React, Typescript) with plain CSS  
- **Backend**: FastAPI (Python) with PostgreSQL  
- **Database script**: `database.sql` (PostgreSQL)

---

## 1. Project Structure

- **frontend** – Next.js app (table UI and filter)
- **backend** – FastAPI app (`/Campaign` endpoint)
- **database.sql** – SQL to create and seed the `campaigns` table

---

## 🚀 Quick Start - Deployment

For detailed deployment instructions, see **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**

**Quick Summary**:
- **Backend**: Deploy to Railway (set root directory to `backend`)
- **Frontend**: Deploy to Vercel (set root directory to `frontend`)
- **Environment Variables**: Set `DATABASE_URL` and `CORS_ORIGINS` in Railway, `NEXT_PUBLIC_API_BASE_URL` in Vercel

---

## 2. Backend (FastAPI)

### 2.1. Environment Setup

Create a `.env` file in the `backend` folder:

```bash
cd backend
```

Create `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:uNqLSPKtRMrQxCTpDdnAgRXFNdpwCcWV@shinkansen.proxy.rlwy.net:51070/railway
CORS_ORIGINS=http://localhost:3000
```

**Note**: Copy `backend/.env.example` to `backend/.env` and update with your actual database URL.

### 2.2. Install and run locally

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

The first time the server runs it will create the `campaigns` table in PostgreSQL and insert 10 sample campaigns.

### 2.3. Deploying backend to Railway

See **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** for detailed instructions.

**Quick steps**:
1. Push repo to GitHub
2. Create new Railway project from GitHub repo
3. Set root directory to `backend`
4. Add environment variables: `DATABASE_URL` and `CORS_ORIGINS`
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy and note the public URL

---

## 3. Database SQL (PostgreSQL / SQLite)

The `database.sql` file creates the `campaigns` table and inserts 10 sample rows.

### 3.1. Example commands

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

### 4.1. Environment Setup

Create a `.env.local` file in the `frontend` folder:

```bash
cd frontend
```

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**Note**: Copy `frontend/.env.example` to `frontend/.env.local` and update with your backend URL.

### 4.2. Install and run locally

From the project root:

```bash
cd frontend
npm install
npm run dev
```

The app will run on `http://localhost:3000`.

Make sure the FastAPI backend is running on port 8000 when you test locally.

### 4.3. Configure API URL (for deployment)

- **Production (Vercel)**: in Vercel project settings, add environment variable:  
  `NEXT_PUBLIC_API_BASE_URL=https://your-railway-app.up.railway.app`

### 4.4. Deploying frontend to Vercel

See **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** for detailed instructions.

**Quick steps**:
1. Push repo to GitHub (if not done)
2. Import project in Vercel from GitHub
3. Set root directory to `frontend`
4. Add environment variable: `NEXT_PUBLIC_API_BASE_URL` (pointing to Railway backend URL)
5. Deploy and note the public URL

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



