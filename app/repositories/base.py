from sqlalchemy.orm import Session
from typing import TypeVar, Generic, List, Optional, Dict, Any
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, 
        skip: int = 0, 
        limit: int = 100,
        **filters
    ) -> List[ModelType]:
        query = self.db.query(self.model)
        
        for field, value in filters.items():
            if value is not None:
                query = query.filter(getattr(self.model, field) == value)
        
        return query.offset(skip).limit(limit).all()

    def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> ModelType:
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        return self.db.query(self.model).filter(getattr(self.model, field) == value).first()
