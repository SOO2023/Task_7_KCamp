from fastapi import HTTPException, status
from sqlalchemy.orm import Session


# CRUD
def get_item_by_id(id: int, db: Session, Model, item_name: str = "item"):
    item = db.query(Model).filter(Model.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"{item_name.capitalize()} with id {id} cannot be found."
            },
        )
    return item


def get_all_items(db: Session, Model):
    items = db.query(Model).all()
    return items


def create_new_item(item_dict: dict, db: Session, Model):
    try:
        item = Model(**item_dict)
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        )
    else:
        return item


def delete_item(id: int, db: Session, Model, item_name: str = "item"):
    get_item_by_id(id, db, Model, item_name)
    item = db.query(Model).filter(Model.id == id).first()
    db.delete(item)
    db.commit()


def update_item(
    id: int, update_dict: dict, db: Session, Model, item_name: str = "item"
):
    get_item_by_id(id, db, Model, item_name)
    item = db.query(Model).filter(Model.id == id)
    try:
        item.update(update_dict)
        db.commit()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": str(error)},
        )
    else:
        return item.first()


def home_page(
    title: str, assignment_desc: str, assignment_details: str, task_no: int
) -> str:
    home = f"""
    <!doctype html>
    <html>
    <head>
    <title>{title}</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    </head>
    <body class="bg-light">
    <div class="container bg-white shadow-sm border border-light rounded" style="margin-top: 80px; padding: 10px;">
    <div class="container text-secondary border-bottom" style="text-align:center;">
    <h1>Task 7 FastAPI Backend - Task {task_no}</h1>
    </div>
    <div class="container" style="margin-top: 30px; padding: 10px;">
    <h4 class="text-body">{assignment_desc}</h4>
    <p>{assignment_details}</p>
    </div>
    </div>
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    return home
