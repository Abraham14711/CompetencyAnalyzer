from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..api import models, schemas
from competencyAnalyser.db.database import get_db

router = APIRouter()


@router.get('/', response_model=List[schemas.QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Question).all()
    return questions


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.QuestionResponse)
def create_question(question: schemas.QuestionCreate,
                    db: Session = Depends(get_db)):
    new_question = models.Question(
        **question.dict()
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


@router.get('/{id}', response_model=schemas.QuestionOut)
def get_question(id: str, db: Session = Depends(get_db)):
    question = db.query(models.Question).filter(
        models.Question.id == id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No question with this id: {id} found")
    return question


@router.put('/{id}', response_model=schemas.QuestionOut)
def update_question(id: str, question: schemas.QuestionUpdate,
                    db: Session = Depends(get_db)):
    question_query = db.query(models.Question).filter(models.Question.id == id)
    db_question = question_query.first()

    if not db_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No question with this id: {id} found')

    question_query.update(question.dict(exclude_unset=True),
                          synchronize_session=False)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.delete('/{id}')
def delete_question(id: str, db: Session = Depends(get_db)):
    question_query = db.query(models.Question).filter(models.Question.id == id)
    question = question_query.first()

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No question with this id: {id} found')

    question_query.delete(synchronize_session=False)
    db.commit()

    return {'status': 'success', 'message': 'Question deleted successfully'}
