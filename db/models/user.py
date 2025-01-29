from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    tg_id: int
    date: datetime


    class Config:
        # Используем alias для работы с _id в MongoDB
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str  # Преобразование ObjectId в строку
        }