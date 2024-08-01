import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..api import models, schemas
from competencyAnalyser.db.database import get_db

router = APIRouter()


@router.get('/', response_model=List[schemas.BusinessTypeOut])
def get_business_types(db: Session = Depends(get_db)):
    business_types = db.query(models.BusinessType).all()
    return business_types


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.BusinessTypeOut)
def create_business_type(business_type: schemas.BusinessTypeCreate,
                         db: Session = Depends(get_db)):
    new_business_type = models.BusinessType(id=uuid.uuid4(),
                                            title=business_type.title)
    db.add(new_business_type)
    db.commit()
    db.refresh(new_business_type)
    return new_business_type


@router.get('/{id}', response_model=schemas.BusinessTypeOut)
def get_business_type(id: str, db: Session = Depends(get_db)):
    business_type = db.query(models.BusinessType).filter(
        models.BusinessType.id == id).first()
    if not business_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No BusinessType with this id: {id} found")
    return business_type


@router.put('/{id}', response_model=schemas.BusinessTypeOut)
def update_business_type(id: str, business_type: schemas.BusinessTypeUpdate,
                         db: Session = Depends(get_db)):
    business_type_query = db.query(models.BusinessType).filter(
        models.BusinessType.id == id)
    db_business_type = business_type_query.first()

    if not db_business_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No BusinessType with this id: {id} found')

    business_type_query.update(business_type.dict(exclude_unset=True),
                               synchronize_session=False)
    db.commit()
    db.refresh(db_business_type)
    return db_business_type


@router.delete('/{id}')
def delete_business_type(id: str, db: Session = Depends(get_db)):
    business_type_query = db.query(models.BusinessType).filter(
        models.BusinessType.id == id)
    business_type = business_type_query.first()

    if not business_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No BusinessType with this id: {id} found')

    business_type_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "BusinessType deleted successfully"}
