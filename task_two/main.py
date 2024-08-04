from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .routers import users, auth, orders, products

from .database import Base, engine
from .util import home_page

Base.metadata.create_all(engine)


title = "E-commerce API"
assignment_desc = "E-commerce API with Comprehensive Testing:"
detail = "Develop an e-commerce API and implement tests for product listing, cart management, order processing, and user authentication. Use both unit tests and end-to-end tests."
html = home_page(title, assignment_desc, detail, 2)


app = FastAPI(
    title=title,
    description="Develop an e-commerce API and implement tests for product listing, cart management, order processing, and user authentication. Use both unit tests and end-to-end tests.",
)


@app.get("/", description="This is the e-commerce API home page", tags=["Home"])
def get_home():
    return HTMLResponse(status_code=200, content=html)


all_routers = [users.router, auth.router, orders.router, products.router]
for router in all_routers:
    app.include_router(router)
