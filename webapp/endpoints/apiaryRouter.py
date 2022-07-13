from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from webapp.containers import Container
from webapp.repositories.notFoundError import NotFoundError
from webapp.services.apiaryService import ApiaryService

apiary_router = APIRouter()


@apiary_router.get("/apiaries")
@inject
def get_list(
        apiary_service: ApiaryService = Depends(Provide[Container.apiary_service]),
):
    return apiary_service.get_apiaries()


@apiary_router.get("/apiaries/{apiary_id}")
@inject
def get_by_id(
        apiary_id: int,
        apiary_service: ApiaryService = Depends(Provide[Container.apiary_service]),
):
    try:
        return apiary_service.get_apiary_by_id(apiary_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@apiary_router.post("/apiaries", status_code=status.HTTP_201_CREATED)
@inject
def add(
        apiary_name: str,
        apiary_service: ApiaryService = Depends(Provide[Container.apiary_service]),
):
    return apiary_service.create_apiary(apiary_name)


@apiary_router.patch("/apiaries/{apiary_id}", status_code=status.HTTP_201_CREATED)
@inject
def update(
        apiary_id: int,
        apiary_name: str,
        apiary_service: ApiaryService = Depends(Provide[Container.apiary_service]),
):
    return apiary_service.update_apiary(apiary_id, apiary_name)


@apiary_router.delete("/apiaries/{apiary_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        apiary_id: int,
        apiary_service: ApiaryService = Depends(Provide[Container.apiary_service]),
):
    try:
        apiary_service.delete_apiary_by_id(apiary_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
