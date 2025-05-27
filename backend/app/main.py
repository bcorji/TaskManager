from fastapi import FastAPI
from app.routes import users_router, projects_router, tasks_router
from app.database import create_tables

app = FastAPI()

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)

@app.get("/")
def root():
    return {"message": "Task Manager API"}
