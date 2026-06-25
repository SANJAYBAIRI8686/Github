from datetime import datetime

from app.schemas.common import ORMModel


class UserRead(ORMModel):
    id: int
    email: str
    created_at: datetime
