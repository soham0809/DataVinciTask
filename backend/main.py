from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, Session

DATABASE_URL = "sqlite:///./campaigns.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()


class CampaignModel(Base):
  __tablename__ = "campaigns"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  status = Column(String, nullable=False)
  clicks = Column(Integer, nullable=False)
  cost = Column(Float, nullable=False)
  impressions = Column(Integer, nullable=False)


class Campaign(BaseModel):
  id: int
  name: str
  status: str
  clicks: int
  cost: float
  impressions: int

  class Config:
    from_attributes = True


def seed_data_if_needed() -> None:
  Base.metadata.create_all(bind=engine)
  with Session(engine) as session:
    count = session.query(CampaignModel).count()
    if count > 0:
      return

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

    session.add_all(sample_campaigns)
    session.commit()


seed_data_if_needed()

app = FastAPI(title="Grippi Campaign API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/campaigns", response_model=List[Campaign])
def get_campaigns() -> List[Campaign]:
  with Session(engine) as session:
    campaigns = session.query(CampaignModel).all()
    return campaigns




