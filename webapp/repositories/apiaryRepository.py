from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from webapp.models.apiary import Apiary
from webapp.repositories.notFoundError import NotFoundError


class ApiaryRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Apiary]:
        with self.session_factory() as session:
            return session.query(Apiary).all()

    def get_by_id(self, apiary_id: int) -> Apiary:
        with self.session_factory() as session:
            apiary = session.query(Apiary).filter(Apiary.id == apiary_id).first()
            if not apiary:
                raise ApiaryNotFoundError(apiary_id)
            return apiary

    def add(self, name: str) -> Apiary:
        with self.session_factory() as session:
            apiary = Apiary(name=name)
            session.add(apiary)
            session.commit()
            session.refresh(apiary)
            return apiary

    def update(self, apiary_id: int, name: str) -> Apiary:
        with self.session_factory() as session:
            apiary = session.get(Apiary, apiary_id)
            if not apiary:
                raise ApiaryNotFoundError(apiary_id)
            apiary.name = name
            session.add(apiary)
            session.commit()
            session.refresh(apiary)
            return apiary

    def delete_by_id(self, apiary_id: int) -> None:
        with self.session_factory() as session:
            entity: Apiary = session.query(Apiary).filter(Apiary.id == apiary_id).first()
            if not entity:
                raise ApiaryNotFoundError(apiary_id)
            session.delete(entity)
            session.commit()


class ApiaryNotFoundError(NotFoundError):
    entity_name: str = "Apiary"
