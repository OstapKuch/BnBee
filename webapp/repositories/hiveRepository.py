from contextlib import AbstractContextManager
from typing import Callable, Iterator

from fastapi import HTTPException
from sqlalchemy.orm import Session

from webapp.models.apiary import Apiary
from webapp.models.hive import Hive
from webapp.repositories.notFoundError import NotFoundError


class HiveRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Hive]:
        with self.session_factory() as session:
            return session.query(Hive).all()

    def get_by_id(self, hive_id: int) -> Hive:
        with self.session_factory() as session:
            hive = session.query(Hive).filter(Hive.id == hive_id).first()
            if not hive:
                raise HiveNotFoundError(hive_id)
            return hive

    def add(self, name: str, is_active: bool, apiary_id: int) -> Hive:
        with self.session_factory() as session:
            entity: Apiary = session.query(Apiary).filter(Apiary.id == apiary_id).first()
            if not entity:
                raise ApiaryNotFoundError(apiary_id)
            hive = Hive(name=name, is_active=is_active, apiary_id=apiary_id)
            session.add(hive)
            session.commit()
            session.refresh(hive)
            return hive

    def update(self, hive_id: int, name: str, bee_count: int, is_active: bool, lid_open: bool, door_open: bool,
               maintenance: bool, apiary_id: int, status: bool) -> Hive:
        with self.session_factory() as session:
            hive = session.get(Hive, hive_id)
            if not hive:
                raise HiveNotFoundError(hive_id)
            hive.name = name
            hive.bee_count = bee_count
            hive.is_active = is_active
            hive.lid_open = lid_open
            hive.door_open = door_open
            hive.maintenance = maintenance
            hive.apiary_id = apiary_id
            hive.status = status
            session.add(hive)
            session.commit()
            session.refresh(hive)
            return hive

    def delete_by_id(self, hive_id: int) -> None:
        with self.session_factory() as session:
            entity: Hive = session.query(Hive).filter(Hive.id == hive_id).first()
            if not entity:
                raise HiveNotFoundError(hive_id)
            session.delete(entity)
            session.commit()


class HiveNotFoundError(NotFoundError):
    entity_name: str = "Hive"


class ApiaryNotFoundError(NotFoundError):
    entity_name: str = "Apiary"
