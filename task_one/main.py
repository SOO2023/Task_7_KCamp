from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routers import router
from .database import Base, engine
from .util import home_page

Base.metadata.create_all(engine)


title = "Task Management API"
assignment_desc = "Task Management API with Unit and Integration Tests:"
detail = "Build a task management API and write unit tests for individual endpoints and integration tests for the overall task creation, update, and deletion process."
html = home_page(title, assignment_desc, detail, 1)


app = FastAPI(
    title=title,
    description="This API is used for creating, updating, deleting, and reading tasks.",
)


@app.get("/", description="This is the API home page", tags=["Home"])
def get_home():
    return HTMLResponse(status_code=200, content=html)


app.include_router(router)
