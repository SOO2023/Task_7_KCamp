from pydantic import BaseModel, Field
from datetime import datetime


class CommentPostOut(BaseModel):
    title: str
    content: str
    date_posted: datetime


class PostCommentOut(BaseModel):
    id: int
    user_id: int
    content: str
    date_commented: datetime


class Comment(BaseModel):
    user_id: int
    post_id: int
    content: str


class CommentIn(Comment):
    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "post_id": 1,
                    "content": "You really had a wonder time in Lagos.",
                }
            ]
        }


class CommentOut(Comment):
    id: int
    content: str
    date_commented: datetime
    post: CommentPostOut

    class ConfigDict:
        from_attributes = True


class Post(BaseModel):
    title: str
    content: str
    image: str | None = None


class PostIn(Post):
    user_id: int

    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "title": "First Time in Lagos.",
                    "content": "As I stepped off the plane in Lagos, the humid air enveloped me, and the sounds of honking horns and lively chatter filled my ears. I was struck by the city's energy and vibrancy. From the bustling streets of Ikeja to the beautiful beaches of Victoria Island, every moment was a new discovery. I savored the flavors of jollof rice and suya, and marveled at the resilience and warmth of the Lagosians. My first experience in Lagos was a whirlwind of excitement, curiosity, and wonder - a city that truly never sleeps!",
                    "image": "abcdef.jpg",
                }
            ]
        }


class PostOut(Post):
    id: int
    user_id: int
    comments: list[PostCommentOut]
    date_posted: datetime

    class ConfigDict:
        from_attributes = True


class User(BaseModel):
    username: str = Field(min_length=3)


class UserIn(User):
    password: str = Field(min_length=4)

    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "username": "sam123",
                    "password": "secret1234",
                }
            ]
        }


class UserOut(User):
    id: int
    posts: list[PostOut]

    class ConfigDict:
        from_attributes = True
