from typing import Iterator

from webapp.models.apiary import Apiary
from webapp.repositories.apiaryRepository import ApiaryRepository


class ApiaryService:

    def __init__(self, apiary_repository: ApiaryRepository) -> None:
        self._repository: ApiaryRepository = apiary_repository

    def get_apiaries(self) -> Iterator[Apiary]:
        return self._repository.get_all()

    def get_apiary_by_id(self, apiary_id: int) -> Apiary:
        return self._repository.get_by_id(apiary_id)

    def create_apiary(self, apiary_name: str) -> Apiary:
        return self._repository.add(name=apiary_name)

    def update_apiary(self, apiary_id: int, apiary_name) -> Apiary:
        return self._repository.update(apiary_id=apiary_id, name=apiary_name)

    def delete_apiary_by_id(self, apiary_id: int) -> None:
        return self._repository.delete_by_id(apiary_id)
