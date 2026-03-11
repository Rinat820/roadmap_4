from typing import List, Any, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from src.database import session_maker


class BaseDAO:
    model = None
    dto = None
    
    @classmethod
    def find_one_or_none(cls, **filter_by) -> Optional[Any]:
        with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = session.execute(query).scalar_one_or_none()
            if result:
                return cls.dto(**result.to_dict())
            return None
            
    @classmethod
    def find_all(cls, **filter_by) -> List[Any]:
        with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            results = session.execute(query).scalars().all()
            return [cls.dto(**row.to_dict()) for row in results]
        
    @classmethod
    def add(cls, **values) -> Any:
        with session_maker() as session:
            new_instance = cls.model(**values)
            session.add(new_instance)
            try:
                session.commit()
                return cls.dto(**new_instance.to_dict())
            except SQLAlchemyError as e:
                session.rollback()
                raise e