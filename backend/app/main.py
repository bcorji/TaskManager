from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users_router, projects_router, tasks_router
from app.routes.categories import router as categories_router
from app.database import create_tables

app = FastAPI(title="TaskManager API")

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5500",  # VS Code Live Server default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()

# Include routers
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(categories_router)

@app.get("/")
def root():
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
