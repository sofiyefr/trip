# 🧭 Travel Planning Website — Development Plan

## 1. Project Overview

**Goal:** Create a responsive web application that helps users plan their trips by selecting destinations, managing itineraries, and booking accommodations or activities.  
**Target Users:** Travelers, tourists, and digital nomads.

---

## 2. Tech Stack

- **Frontend:** HTML, CSS, JavaScript 
- **Backend:** Python 
- **Database:** sqlite
- **Authentication:** JWT / OAuth 2.0 (Google login optional)
- **Hosting:** 
  - Frontend: Vercel / Netlify  
  - Backend: Render / Heroku

---

## 3. Key Features

### 3.1 User Features
- ✅ User registration and login
- ✅ Profile management
- ✅ Trip creation and editing
- ✅ Destination search with filtering
- ✅ Interactive itinerary builder (calendar-style)
- ✅ Notes and reminders
- ✅ Travel budget tracker
- ✅ Share trips with friends

### 3.2 Admin Features
- ✅ Manage destinations database
- ✅ View user activity
- ✅ Moderate content

---

## 4. Pages / Components Structure

- Home Page
- Login / Signup Page
- User Dashboard
- Trip Planner Page
- Destination Search Page
- Itinerary View Page
- Admin Panel
- 404 / Error Pages

---

## 5. Project Structure
```
travel-planner/
│
├── client/                        # Frontend (plain js)
│   ├── public/
│   ├── src/
│   │   ├── components/            # Reusable UI components
│   │   ├── pages/                 # Route-based pages
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── context/               # Context API for state management
│   │   ├── services/              # API service calls
│   │   ├── styles/                # Global and component-specific styles
│   │   ├── assets/                # Images, icons, fonts
│   │   └── main.jsx               # Main entry file
│   └── package.json
│
├── server/                        # Backend (Flask)
│   ├── app/                       # Main application package
│   │   ├── __init__.py            # Flask app initialization
│   │   ├── routes/                # API route definitions
│   │   ├── controllers/           # Business logic
│   │   ├── models/                # SQLAlchemy models
│   │   └── utils/                 # Helper functions, validation
│   ├── config.py                  # App configuration
│   ├── requirements.txt           # Python dependencies
│   └── run.py                     # Entry point to start Flask server
│
├── .env                           # Environment variables
├── README.md                      # Project documentation
└── database_setup.sql             # Optional: initial DB schema
```
---

## 6. Development Phases

### Phase 1: Environment Setup
- Initialize Git repository
- Setup frontend (plain js) and backend (Flask)
- Configure sqlite and connect to backend
- Setup routing between frontend and backend

### Phase 2: Core Functionalities
- User registration and authentication (JWT)
- Trip CRUD functionality
- Destination search and filters
- Calendar or list-based itinerary

### Phase 3: Extra User Features
- Budget tracker with totals and categories
- Notes and personal reminders per trip
- Trip sharing (link-based or by username)

### Phase 4: Admin Panel & Security
- Admin interface for managing destination data
- Content moderation tools
- Secure API endpoints and validation

### Phase 5: Deployment & Finalization
- Final bug fixes
- Deployment of backend (Render/Railway)
- Deployment of frontend (Netlify/Vercel)
- Final usability testing

---

## 7. Optional Features

- 🗺️ Google Maps or Leaflet integration
- 🌤️ Weather API integration per destination
- 💸 Currency converter
- 📨 Email notifications or reminders
- 🧑‍🤝‍🧑 Collaborative trip planning with friends

---

## 8. Milestones

| Milestone | Description                        | Deadline  |
|-----------|------------------------------------|-----------|
| M1        | Initial project setup              | [Insert]  |
| M2        | Auth system & user dashboard       | [Insert]  |
| M3        | Trip planner & search functionality| [Insert]  |
| M4        | Budget, notes, and itinerary       | [Insert]  |
| M5        | Admin panel & deployment           | [Insert]  |

---

## 9. Contributors

- Frontend: [Sofia Yefremova]
- Backend: [Sofia Yefremova]
- UI/UX Design: [Sofia Yefremova]

---

## 10. License

This project is licensed under the MIT License.
