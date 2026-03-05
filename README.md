# 🏀 NBA Predictor & Stats

A full-stack web application that combines real-time NBA data with a machine learning model to predict game outcomes. Built with Angular, .NET, and Python.

---

## Overview

NBA Predictor & Stats is a personal project built out of a genuine interest in basketball analytics. It pulls live data directly from the NBA API, runs it through a trained ML model, and presents everything through a clean, dark-themed interface inspired by NBA branding.

The app has four main sections — live standings, league leaders, team leaders, and the game predictor — all accessible from a persistent navigation bar with a live score ticker running across the top.

---

## Features

### 🔮 Game Predictor
Select any two NBA teams and get an AI-generated prediction for the outcome. The predictor shows the projected final score, a confidence percentage based on the model's probability output, and a full head-to-head history pulled from matchup data spanning 2020–2025. Teams can be toggled between Home and Away before running a prediction, since home-court advantage is factored into the model.

### 📊 Standings
Real-time Eastern and Western Conference standings fetched from the NBA API. Every column in the table is sortable — click W, L, PCT, GB, or any other header to rank teams instantly. Clicking the same column again reverses the sort direction.

### 🏆 League Leaders
Top 5 players per statistical category for the current season — points, assists, rebounds, steals, blocks, and minutes per game. Data is fetched in parallel across all categories for fast load times.

### 🏟️ Team Leaders
Top 5 teams per category — points, assists, rebounds, steals, blocks, and field goal percentage. Useful for a quick glance at which franchises are dominating each area of the game.

### 📡 Live Score Ticker
A scrolling ticker pinned below the header shows all of today's games with live scores. Games currently in progress are highlighted in gold with a pulsing live indicator. The ticker auto-refreshes every 60 seconds and pauses on hover.

---

## The ML Model

The prediction model was trained on over 5 years of NBA matchup data (2020–2025), covering all regular season games. Three separate models handle different aspects of each prediction:

- **Winner classifier** — predicts which team wins, outputs a probability used for the confidence score
- **Winner score regressor** — predicts the winning team's final point total
- **Loser score regressor** — predicts the losing team's final point total

Input features include per-team averages for field goal percentage, three-point percentage, free throw percentage, assists, rebounds, steals, blocks, turnovers, plus/minus, and recent form (W/L ratio over the last 10 games), along with one-hot encoded team identities. The model is trained as team1 (home) vs team2 (away), so the Home/Away toggle in the UI directly affects the prediction.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Angular 18 (standalone components) |
| Backend | .NET 8 / ASP.NET Core Web API |
| Prediction Service | Python · FastAPI · Uvicorn |
| ML Model | scikit-learn · pandas · joblib |
| Data | NBA API (`nba_api` Python package) |
| Styling | Custom CSS · Barlow Condensed · NBA colour palette |

---

## Architecture

```
┌─────────────────────────────────────┐
│           Angular Frontend          │
│  Standings · Leaders · Predictor    │
│           Score Ticker              │
└────────────────┬────────────────────┘
                 │ HTTP (REST)
┌────────────────▼────────────────────┐
│        .NET ASP.NET Core API        │
│  /api/standings  /api/scores        │
│  /api/leagueleaders                 │
│  /api/teamleaders                   │
│  /api/prediction/predict            │
└──────┬─────────────────┬────────────┘
       │ spawn process   │ HTTP POST
┌──────▼──────┐   ┌──────▼──────────────┐
│ fetch_data  │   │   FastAPI Service    │
│    .py      │   │   predict_api.py     │
│  NBA API    │   │  scikit-learn model  │
└─────────────┘   └──────────────────────┘
```

The backend acts as a thin orchestration layer. For live data it spawns `fetch_data.py`, which handles caching (1-hour TTL for standings/leaders, 60-second TTL for scores) so the NBA API is never hammered on repeated requests. Predictions are routed to a dedicated FastAPI microservice that loads the trained model once at startup and keeps it in memory — reducing prediction latency from ~10s to ~100ms. All cache files are automatically invalidated and regenerated if they become corrupt or stale.

---

## Data & Caching

Live data is cached on disk to avoid rate-limiting from the NBA API:

| Endpoint | Cache TTL |
|---|---|
| Standings | 1 hour |
| League Leaders | 1 hour |
| Team Leaders | 1 hour |
| Today's Scores | 60 seconds |

The current NBA season is detected automatically based on the current date — the app does not require a manual season update when a new season starts.

---

*Data provided by the NBA API. This project is not affiliated with or endorsed by the NBA.*
