from typing import Any, Generic, Type, TypeVar
# from sqlalchemy.orm import Session
# from db.base_class import Base

# ModelType = TypeVar("ModelType", bound=Base)

class BaseService:
    # def __init__(self, model: Type[ModelType]):
    #     self.model = model

    def get_all(self, db: Any) -> Any:
        # return db.query(self.model).all()
        return []
