import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..api import models, schemas
from competencyAnalyser.db.database import get_db

router = APIRouter()


@router.get('/', response_model=List[schemas.VacancyOut])
def get_vacancies(db: Session = Depends(get_db)):
    vacancies = db.query(models.Vacancy).all()
    return vacancies


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.VacancyOut)
def create_vacancy(vacancy: schemas.VacancyCreate,
                   db: Session = Depends(get_db)):
    new_vacancy = models.Vacancy(id=uuid.uuid4(), title=vacancy.title)

    business_types = db.query(models.BusinessType).filter(
        models.BusinessType.id.in_(vacancy.business_type_ids)).all()
    if len(business_types) != len(vacancy.business_type_ids):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="One or more BusinessType not found")

    new_vacancy.business_types = business_types

    db.add(new_vacancy)
    db.commit()
    db.refresh(new_vacancy)
    return new_vacancy


@router.get('/{id}', response_model=schemas.VacancyOut)
def get_vacancy(id: str, db: Session = Depends(get_db)):
    vacancy = db.query(models.Vacancy).filter(models.Vacancy.id == id).first()
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No vacancy with this id: {id} found")
    return vacancy


@router.put('/{id}', response_model=schemas.VacancyOut)
def update_vacancy(id: str, vacancy: schemas.VacancyUpdate,
                   db: Session = Depends(get_db)):
    vacancy_query = db.query(models.Vacancy).filter(models.Vacancy.id == id)
    db_vacancy = vacancy_query.first()

    if not db_vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No vacancy with this id: {id} found')

    if vacancy.business_type_ids:
        business_types = db.query(models.BusinessType).filter(
            models.BusinessType.id.in_(vacancy.business_type_ids)).all()
        if len(business_types) != len(vacancy.business_type_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="One or more BusinessType not found")
        db_vacancy.business_types = business_types

    vacancy_query.update(vacancy.dict(exclude_unset=True),
                         synchronize_session=False)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


@router.delete('/{id}')
def delete_vacancy(id: str, db: Session = Depends(get_db)):
    vacancy_query = db.query(models.Vacancy).filter(models.Vacancy.id == id)
    vacancy = vacancy_query.first()

    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No vacancy with this id: {id} found')

    vacancy_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Vacancy deleted successfully"}
