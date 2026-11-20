# RideBook AI

RideBook is a comprehensive, multi-modal transport and ride-booking platform powered by Django. It provides an intelligent routing engine to suggest the best travel options (Bike, Auto, Cab, Bus, Train, Flight) based on distance, budget, and passenger requirements.

## Features

- **User Portal**: Route search, multi-modal booking, trip management, and emergency contacts.
- **Driver Portal**: Real-time ride acceptance, OTP verification, and earnings tracking.
- **Admin Console**: Real-time monitoring of users, drivers, active bookings, refunds, and emergency SOS alerts.
- **Smart AI Route Planner**: Automatic calculations for first-mile, long-distance, and last-mile transit.
- **Live Ride Tracking**: Active journey tracking and verification.
- **Emergency Alerts**: Built-in real-time SOS tracking.

## Technology Stack

- **Backend**: Python 3.14 & Django 6.0+
- **Database**: SQLite (`ridebook.db`) with complete Django ORM mapping (`rides/models.py`)
- **Frontend**: Responsive UI templates with Jinja2 / Django engine
- **External APIs**: OSRM (Open Source Routing Machine), OpenStreetMap Nominatim

## Getting Started

1. **Start the Django Server**:
   ```cmd
   Start_App.bat
   ```
   Or directly via CLI:
   ```cmd
   python manage.py runserver 0.0.0.0:5000
   ```
2. **Stop Server**:
   ```cmd
   Stop_Server.bat
   ```
3. **Access Portals**:
   - Web App: `http://localhost:5000/`
   - User Login: `http://localhost:5000/login`
   - Driver Login: `http://localhost:5000/driver-login`
   - Admin Login: `http://localhost:5000/admin-login` (Username: `Admin` or `admin@ridebook.ai`, Password: `admin123`)
