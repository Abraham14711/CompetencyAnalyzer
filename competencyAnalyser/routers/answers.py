from ..api import models, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from competencyAnalyser.db.database import get_db

router = APIRouter()


@router.get('/', response_model=schemas.AnswerListResponse)
def get_answers(db: Session = Depends(get_db)):
    answers = db.query(models.Answer).group_by(models.Answer.id).all()
    return {'status': 'success', 'results': len(answers), 'answers': answers}


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.AnswerResponse)
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    new_answer = models.Answer(
        **answer.dict()
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


@router.put('/{id}', response_model=schemas.AnswerResponse)
def update_answer(
        id: str,
        answer: schemas.AnswerUpdate,
        db: Session = Depends(get_db)):
    answer_query = db.query(models.Answer).filter(models.Answer.id == id)
    existing_answer = answer_query.first()
    answer_query.update(answer.dict(exclude_unset=True),
                        synchronize_session=False)
    db.commit()
    db.refresh(existing_answer)
    return existing_answer


@router.get('/{id}', response_model=schemas.AnswerResponse)
def get_answer(id: str, db: Session = Depends(get_db)):
    answer = db.query(models.Answer).filter(models.Answer.id == id).first()
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No answer with this id: {id} found")
    return answer


@router.delete('/{id}')
def delete_answer(id: str, db: Session = Depends(get_db)):
    answer_query = db.query(models.Answer).filter(models.Answer.id == id)

    answer_query.delete(synchronize_session=False)
    db.commit()

    return {'status': 'success', 'message': 'Answer deleted successfully'}
