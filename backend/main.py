# backend/main.py
import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Path as PathParam
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session as SASession

# Load .env if present (for local dev where you place the production DATABASE_URL)
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    # Read and parse manually to handle BOM if present
    content = env_path.read_text(encoding='utf-8-sig')  # utf-8-sig strips BOM
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required. Set it in backend/.env or export it.")

# Use the provided DATABASE_URL (Postgres). No sqlite fallback.
# Ensure psycopg2-binary is installed
connect_args = {}  # no sqlite check_same_thread
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


class CampaignModel(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    clicks = Column(Integer, nullable=False, default=0)
    cost = Column(Float, nullable=False, default=0.0)
    impressions = Column(Integer, nullable=False, default=0)


class Campaign(BaseModel):
    id: int
    name: str
    status: str
    clicks: int
    cost: float
    impressions: int

    class Config:
        from_attributes = True


# Do NOT call create_all blindly in heavy production; for this assignment it's acceptable
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Grippi Campaign API (Postgres-only)")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CampaignCreate(BaseModel):
    name: str
    status: str = "Active"  # Default status


@app.get("/campaigns", response_model=List[Campaign])
def get_campaigns(
    status: Optional[str] = Query(None, description="Filter by status: Active or Paused"),
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=1000),
):
    offset = (page - 1) * limit
    with SessionLocal() as session:  # type: SASession
        q = session.query(CampaignModel)
        if status:
            status = status.capitalize()
            if status not in ("Active", "Paused"):
                raise HTTPException(status_code=400, detail="status must be 'Active' or 'Paused'")
            q = q.filter(CampaignModel.status == status)
        campaigns = q.offset(offset).limit(limit).all()
        return campaigns


@app.post("/campaigns", response_model=Campaign, status_code=201)
def create_campaign(campaign_data: CampaignCreate):
    """Create a new campaign with default values (clicks=0, cost=0, impressions=0)."""
    with SessionLocal() as session:  # type: SASession
        # Validate status
        if campaign_data.status not in ("Active", "Paused"):
            raise HTTPException(status_code=400, detail="status must be 'Active' or 'Paused'")
        
        # Fix sequence if it's out of sync (in case manual inserts were made)
        try:
            session.execute(text(
                "SELECT setval('campaigns_id_seq', COALESCE((SELECT MAX(id) FROM campaigns), 1), true)"
            ))
            session.commit()
        except Exception:
            # If sequence doesn't exist or error occurs, continue anyway
            session.rollback()
        
        new_campaign = CampaignModel(
            name=campaign_data.name,
            status=campaign_data.status,
            clicks=0,
            cost=0.0,
            impressions=0,
        )
        session.add(new_campaign)
        session.commit()
        session.refresh(new_campaign)
        return new_campaign


@app.patch("/campaigns/{campaign_id}/toggle-status", response_model=Campaign)
def toggle_campaign_status(campaign_id: int = PathParam(..., description="Campaign ID")):
    """Toggle campaign status between Active and Paused."""
    with SessionLocal() as session:  # type: SASession
        campaign = session.query(CampaignModel).filter(CampaignModel.id == campaign_id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Toggle status
        campaign.status = "Paused" if campaign.status == "Active" else "Active"
        session.commit()
        session.refresh(campaign)
        return campaign
