from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .routers import comments, posts, users, auth
from .database import Base, engine
from .util import home_page

Base.metadata.create_all(engine)


title = "Blog API"
assignment_desc = "Blog API with Authentication Testing:"
detail = "Create a blog API with user authentication and write tests for user registration, login, post creation, updating, deletion, and commenting. Ensure secure access control with proper testing."
html = home_page(title, assignment_desc, detail, 3)


app = FastAPI(
    title=title,
    description="This blog API contains user authentication, user registration, login, post creation, updating, deletion, and commenting of blog posts.",
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", description="This is the blog API home page", tags=["Home"])
def get_home():
    return HTMLResponse(status_code=200, content=html)


all_routers = [users.router, auth.router, posts.router, comments.router]
for router in all_routers:
    app.include_router(router)
