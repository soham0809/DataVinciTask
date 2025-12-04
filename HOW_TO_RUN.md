# How to Run the Project

## Quick Start Guide

You need to run **two things**: the backend (FastAPI) and the frontend (Next.js).

---

## Step 1: Run the Backend (FastAPI)

Open **PowerShell** or **Command Prompt** and run:

```powershell
# Navigate to backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Success**: You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal window open!** The backend needs to keep running.

**Test it**: Open your browser and go to:
- API: http://localhost:8000/campaigns
- API Docs: http://localhost:8000/docs

---

## Step 2: Run the Frontend (Next.js)

Open a **NEW** PowerShell/Command Prompt window and run:

```powershell
# Navigate to frontend folder
cd frontend

# Install dependencies (first time only)
npm install

# Run the development server
npm run dev
```

✅ **Success**: You should see:
```
- ready started server on 0.0.0.0:3000
- Local: http://localhost:3000
```

**Open your browser**: Go to http://localhost:3000

You should see the Campaign Analytics Dashboard with a table showing 10 campaigns!

---

## Step 3: Test the Filter

1. On the dashboard page, you'll see a dropdown that says "Status filter"
2. Try selecting:
   - **All** - Shows all 10 campaigns
   - **Active** - Shows only Active campaigns
   - **Paused** - Shows only Paused campaigns

---

## Troubleshooting

### Backend Issues

**Problem**: `python` command not found
- **Solution**: Make sure Python is installed. Try `python3` instead of `python`, or install Python from python.org

**Problem**: Port 8000 already in use
- **Solution**: Change the port: `uvicorn main:app --reload --host 0.0.0.0 --port 8001`
- Then update frontend: Create `frontend/.env.local` with: `NEXT_PUBLIC_API_BASE_URL=http://localhost:8001`

**Problem**: `pip` command not found
- **Solution**: Use `python -m pip` instead of `pip`

### Frontend Issues

**Problem**: `npm` command not found
- **Solution**: Install Node.js from nodejs.org

**Problem**: Frontend shows "Error: Failed to load campaigns"
- **Solution**: Make sure the backend is running on port 8000 first!

**Problem**: Port 3000 already in use
- **Solution**: Next.js will automatically use the next available port (like 3001)

---

## What's Happening?

1. **Backend** (`backend/main.py`):
   - Creates a SQLite database file (`campaigns.db`) automatically
   - Inserts 10 sample campaigns on first run
   - Provides API endpoint at `/campaigns`

2. **Frontend** (`frontend/pages/index.tsx`):
   - Fetches data from `http://localhost:8000/campaigns`
   - Displays campaigns in a table
   - Filters by status (All/Active/Paused)

---

## Stop the Servers

- Press `Ctrl + C` in each terminal window to stop the servers

