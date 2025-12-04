# Campaign Analytics Dashboard

A full-stack web application for managing and analyzing marketing campaigns. Built with Next.js and FastAPI, this dashboard provides real-time campaign metrics, status management, and filtering capabilities.

## 🎯 Overview

The Campaign Analytics Dashboard is a simplified version of a marketing campaign management system. It allows users to view, create, and manage marketing campaigns with real-time status updates and comprehensive analytics.

## ✨ Features

- **Campaign Management**: Create, view, and manage marketing campaigns
- **Status Toggle**: Switch campaigns between Active and Paused states with a single click
- **Real-time Filtering**: Filter campaigns by status (All, Active, Paused)
- **Campaign Metrics**: Track clicks, cost, and impressions for each campaign
- **Responsive Design**: Modern, dark-themed UI that works on all devices
- **RESTful API**: Clean API endpoints for campaign operations

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 14 with React and TypeScript
- **Styling**: Custom CSS with dark theme
- **State Management**: React Hooks (useState, useEffect)
- **API Integration**: Fetch API for backend communication

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (hosted on Railway)
- **ORM**: SQLAlchemy for database operations
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

### Database
- **Type**: PostgreSQL
- **Schema**: Single `campaigns` table with fields for name, status, clicks, cost, and impressions

## 📊 Data Model

### Campaign
Each campaign contains:
- **ID**: Unique identifier (auto-incremented)
- **Name**: Campaign name
- **Status**: Either "Active" or "Paused"
- **Clicks**: Number of clicks (default: 0)
- **Cost**: Campaign cost in USD (default: 0.00)
- **Impressions**: Number of impressions (default: 0)

## 🔌 API Endpoints

### `GET /Campaign`
Retrieves all campaigns with optional filtering and pagination.

**Response**: Array of campaign objects

### `POST /Campaign`
Creates a new campaign with default values.

**Request Body**:
```json
{
  "name": "Campaign Name",
  "status": "Active"
}
```

**Response**: Created campaign object with auto-generated ID

### `PATCH /Campaign/{id}/toggle-status`
Toggles a campaign's status between Active and Paused.

**Response**: Updated campaign object

## 🎨 User Interface

The dashboard features:
- **Campaign Table**: Displays all campaigns with their metrics
- **Add Campaign Button**: Opens a form to create new campaigns
- **Status Filter Dropdown**: Filter campaigns by status
- **Toggle Buttons**: Click any status button to switch between Active/Paused
- **Loading States**: Visual feedback during API operations
- **Error Handling**: User-friendly error messages

## 🔐 Environment Configuration

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `CORS_ORIGINS`: Allowed frontend origins (comma-separated)

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL

## 📁 Project Structure

```
DataVinci/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── seed_data.py         # Database seeding script
│   ├── requirements.txt      # Python dependencies
│   └── .env                 # Environment variables (not in git)
├── frontend/
│   ├── pages/
│   │   ├── _app.tsx         # Next.js app wrapper
│   │   ├── index.tsx        # Home page (redirects)
│   │   └── Campaign.tsx      # Campaign dashboard page
│   ├── styles/
│   │   └── globals.css      # Global styles
│   └── package.json         # Node.js dependencies
├── database.sql             # Database schema and seed data
└── README.md               # This file
```

## 🛠️ Technology Stack

- **Frontend**: Next.js, React, TypeScript, CSS
- **Backend**: FastAPI, Python, SQLAlchemy
- **Database**: PostgreSQL
- **Deployment**: Vercel (frontend), Railway (backend)


