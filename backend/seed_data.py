"""
Script to seed the PostgreSQL database with sample campaign data.
Run this once to populate the database.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load .env file FIRST before any imports
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    # Read file directly and parse manually (handle BOM if present)
    content = env_path.read_text(encoding='utf-8-sig')  # utf-8-sig strips BOM
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            os.environ[key] = value

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

# Define the model here to avoid circular import
Base = declarative_base()


class CampaignModel(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    clicks = Column(Integer, nullable=False, default=0)
    cost = Column(Float, nullable=False, default=0.0)
    impressions = Column(Integer, nullable=False, default=0)

# Create engine and session
engine = create_engine(DATABASE_URL, connect_args={}, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Sample campaigns data
sample_campaigns = [
    CampaignModel(
        id=1,
        name="Summer Sale",
        status="Active",
        clicks=150,
        cost=45.99,
        impressions=1000,
    ),
    CampaignModel(
        id=2,
        name="Black Friday",
        status="Paused",
        clicks=320,
        cost=89.50,
        impressions=2500,
    ),
    CampaignModel(
        id=3,
        name="New Year Blast",
        status="Active",
        clicks=210,
        cost=60.00,
        impressions=1800,
    ),
    CampaignModel(
        id=4,
        name="Spring Clearance",
        status="Paused",
        clicks=90,
        cost=25.75,
        impressions=900,
    ),
    CampaignModel(
        id=5,
        name="Back to School",
        status="Active",
        clicks=300,
        cost=99.99,
        impressions=2700,
    ),
    CampaignModel(
        id=6,
        name="Holiday Specials",
        status="Active",
        clicks=180,
        cost=55.25,
        impressions=1500,
    ),
    CampaignModel(
        id=7,
        name="Clearance Bonanza",
        status="Paused",
        clicks=75,
        cost=19.99,
        impressions=800,
    ),
    CampaignModel(
        id=8,
        name="Weekend Flash Sale",
        status="Active",
        clicks=260,
        cost=70.10,
        impressions=2200,
    ),
    CampaignModel(
        id=9,
        name="Referral Program",
        status="Active",
        clicks=140,
        cost=40.00,
        impressions=1200,
    ),
    CampaignModel(
        id=10,
        name="Loyalty Rewards",
        status="Paused",
        clicks=110,
        cost=35.50,
        impressions=950,
    ),
]


def seed_database():
    """Seed the database with sample campaigns."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as session:
        # Check if data already exists
        count = session.query(CampaignModel).count()
        if count > 0:
            print(f"Database already has {count} campaigns. Skipping seed.")
            print("To re-seed, delete existing data first.")
            return
        
        # Insert sample campaigns
        session.add_all(sample_campaigns)
        session.commit()
        print(f"Successfully seeded {len(sample_campaigns)} campaigns into the database!")


if __name__ == "__main__":
    seed_database()

