from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..api import models, schemas
from competencyAnalyser.db.database import get_db

router = APIRouter()


@router.get('/', response_model=List[schemas.CompetencyOut])
def get_competencies(db: Session = Depends(get_db)):
    competencies = db.query(models.Competency).all()
    return competencies


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.CompetencyOut)
def create_competency(competency: schemas.CompetencyCreate,
                      db: Session = Depends(get_db)):
    new_competency = models.Competency(**competency.dict())
    db.add(new_competency)
    db.commit()
    db.refresh(new_competency)
    return new_competency


@router.get('/{id}', response_model=schemas.CompetencyOut)
def get_competency(id: str, db: Session = Depends(get_db)):
    competency = db.query(models.Competency).filter(
        models.Competency.id == id).first()
    if not competency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No competency with this id: {id} found")
    return competency


@router.put('/{id}', response_model=schemas.CompetencyOut)
def update_competency(id: str, competency: schemas.CompetencyUpdate,
                      db: Session = Depends(get_db)):
    competency_query = db.query(models.Competency).filter(
        models.Competency.id == id)
    db_competency = competency_query.first()

    if not db_competency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No competency with this id: {id} found')

    competency_query.update(competency.dict(exclude_unset=True),
                            synchronize_session=False)
    db.commit()
    db.refresh(db_competency)
    return db_competency


@router.delete('/{id}')
def delete_competency(id: str, db: Session = Depends(get_db)):
    competency_query = db.query(models.Competency).filter(
        models.Competency.id == id)
    competency = competency_query.first()

    if not competency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No competency with this id: {id} found')

    competency_query.delete(synchronize_session=False)
    db.commit()

    return {'status': 'success', 'message': 'Competency deleted successfully'}
