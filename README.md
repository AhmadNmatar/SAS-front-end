# Smart Attendance System (SAS)

A modern, web-based attendance management system using facial recognition technology. Built with Flask, this frontend application interfaces with a backend API to provide real-time attendance tracking and student enrollment.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.2-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **🔐 Secure Authentication** - Login system with session management
- **👤 Face Enrollment** - Enroll new students/employees via camera
- **📸 Real-time Attendance** - Automatic attendance taking using facial recognition
- **📊 Live Dashboard** - View attendance records in real-time
- **📱 Responsive Design** - Works on desktop and mobile devices

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Smart Attendance System               │
├─────────────────────────────────────────────────────────┤
│  Frontend (This Repository)                              │
│  ├── Flask Web Server                                    │
│  ├── HTML/CSS Templates                                  │
│  └── JavaScript for Camera & API Calls                   │
├─────────────────────────────────────────────────────────┤
│  Backend API (Separate Repository)                       │
│  ├── Facial Recognition Engine                           │
│  ├── Database Management                                 │
│  └── Authentication Services                             │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
SAS-front-end/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── static/
│   │   ├── attendance.js        # Camera & attendance logic
│   │   └── style.css            # Global styles
│   └── templates/
│       ├── base.html            # Base template with navigation
│       ├── login.html           # Login page
│       ├── dashboard.html       # Main dashboard
│       ├── enrollment.html      # Face enrollment page
│       └── attendance.html      # Real-time attendance page
├── instance/                    # Flask instance folder
├── requirement.txt              # Python dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- A backend server running the SAS API
- Modern web browser with camera support

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SAS-front-end.git
   cd SAS-front-end
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   BACKEND_URL=http://localhost:5001  # URL of your backend API
   ```

5. **Run the application**
   ```bash
   flask run
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📖 Usage Guide

### Login
- Navigate to the login page
- Enter your admin credentials
- Click "Login" to access the dashboard

### Dashboard
The dashboard provides two main options:
- **Take Attendance** - Opens the real-time attendance camera
- **Enroll** - Opens the face enrollment form

### Enrolling a New Person
1. Click "Enroll" on the dashboard
2. Enter the person's first name and last name
3. Submit the form
4. The backend will handle camera capture for face enrollment

### Taking Attendance
1. Click "Take Attendance" on the dashboard
2. Click "Start" to activate the camera
3. The system will automatically:
   - Capture frames from your camera
   - Send them to the backend for facial recognition
   - Display recognized individuals in the attendance table
4. Click "Stop" when finished to mark remaining people as absent

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `BACKEND_URL` | URL of the SAS backend API | Yes |

### Backend Requirements

This frontend requires a compatible backend API running. Ensure your backend provides:

- `POST /admin/login` - Admin authentication
- `POST /attendance/enroll_camera` - Face enrollment
- `POST /attendance/take_attendance` - Process frame for attendance
- `GET /attendance/absent` - Get list of absent people

## 🛠️ Tech Stack

- **Backend Framework**: Flask 3.1.2
- **Configuration**: python-dotenv 1.2.1
- **HTTP Client**: requests
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Browser APIs**: MediaDevices, Canvas, Fetch

## 📝 API Endpoints

### Frontend Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home/Redirect to login or dashboard |
| `/login` | GET/POST | Admin login page |
| `/logout` | GET | Logout and clear session |
| `/dashboard` | GET | Main dashboard |
| `/enrollment` | GET | Face enrollment page |
| `/enroll` | POST | Submit enrollment data |
| `/attendance` | GET | Real-time attendance page |
| `/api/config` | GET | Get frontend configuration |

## 🎨 UI Features

- Clean, modern interface
- Responsive navigation bar
- Real-time status updates
- Attendance table with scrolling
- Camera preview with overlay
- Start/Stop controls for attendance capture

## 🔒 Security Notes

- Session-based authentication with JWT tokens
- All API requests include Authorization header
- Backend URL should be kept confidential
- Use HTTPS in production environments



