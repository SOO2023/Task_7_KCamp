from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .util import home_page
from .routers import auth, authors, users, books, borrow
from .database import Base, engine


Base.metadata.create_all(engine)


title = "Library Management API"
assignment_desc = "Library Management API with CRUD Tests:"
detail = "Build a library management API and implement tests for CRUD operations on books, authors, and borrow records. Ensure that relationships between entities are correctly handled in tests."
html = home_page(title, assignment_desc, detail, 4)


app = FastAPI(
    title=title,
    description="This API enables CRUD operations on books, authors, and borrow records.",
)


@app.get("/", description="This is the API home page", tags=["Home"])
def get_home():
    return HTMLResponse(status_code=200, content=html)


all_routers = [authors.router, users.router, books.router, auth.router, borrow.router]
for router in all_routers:
    app.include_router(router)
