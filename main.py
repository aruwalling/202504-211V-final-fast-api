from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import health, students, root

app = FastAPI(
    title="Students API",
    description="API with FastAPI, Jinja2 and MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

templates = Jinja2Templates(directory="templates")
app.state.templates = templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(root.router, tags=["Root"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(students.router, prefix="/students", tags=["Students"])
