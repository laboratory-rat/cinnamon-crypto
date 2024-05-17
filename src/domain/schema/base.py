import uuid

from pydantic import BaseModel


class BaseEntitySchema(BaseModel):
    id: uuid.UUID = None
    created_at: float = None
    updated_at: float = None
