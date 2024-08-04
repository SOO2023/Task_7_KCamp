from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    description: str
    content: str


class TaskIn(Task):
    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "description": "Push ups",
                    "content": "I want to do at least 1000 push ups before the week runs out",
                }
            ]
        }


class TaskUpdate(Task):
    completed: bool

    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "description": "Push ups",
                    "content": "I want to do at least 1000 push ups before the week runs out",
                    "completed": False,
                }
            ]
        }


class TaskOut(Task):
    id: int
    completed: bool
    date: datetime

    class ConfigDict:
        from_attributes = True
