# TaskManager

A modern task management application built with FastAPI and a responsive web frontend.

## Features

- User Authentication with JWT tokens
- Task Management (Create, Read, Update, Delete)
- Task categorization (To Do, In Progress, Completed)
- Priority levels (Low, Medium, High)
- Due dates tracking
- Real-time updates
- Responsive design with TailwindCSS

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- Alembic (Database migrations)
- PostgreSQL (Database)
- JWT Authentication
- Pydantic (Data validation)

### Frontend
- HTML5
- TailwindCSS (Styling)
- JavaScript (ES6+)
- Fetch API (HTTP requests)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js (for TailwindCSS)
- PostgreSQL

### Installation

1. Clone the repository:
```powershell
git clone https://github.com/bcorji/TaskManager.git
cd TaskManager
```

2. Set up the backend:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the database:
```powershell
alembic upgrade head
```

4. Run the backend server:
```powershell
python -m uvicorn app.main:app --reload
```

5. Open another terminal and serve the frontend:
```powershell
cd frontend
python -m http.server 8080
```

6. Visit `http://localhost:8080` in your browser

## Project Structure

```
TaskManager/
├── backend/              # FastAPI backend
│   ├── alembic/         # Database migrations
│   ├── app/             # Application code
│   │   ├── routes/      # API endpoints
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # Pydantic models
│   │   └── main.py      # Application entry point
│   └── requirements.txt  # Python dependencies
└── frontend/            # Frontend code
    ├── js/             # JavaScript code
    │   └── services/   # API and Auth services
    ├── pages/          # HTML pages
    └── index.html      # Landing page
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details