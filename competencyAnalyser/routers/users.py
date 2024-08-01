import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import RedirectResponse

from .main import app_language
from ..api import models, schemas
from competencyAnalyser.db.database import get_db
from competencyAnalyser.config import templates
from competencyAnalyser.scripts.auth_functions import (check_authorized,
                                                       get_params)
from ..scripts.ai import generate_user_description
from ..scripts.translator import TranslatorI18n
from ..scripts.verifyTheHash import verify_telegram_authentication

router = APIRouter()


@router.get('/', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with this id: {id} found")
    return user


@router.delete('/{id}')
def delete_user(id: str, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this id: {id} found')

    user_query.delete(synchronize_session=False)
    db.commit()

    return {'status': 'success', 'message': 'User deleted successfully'}


@router.get("/show/{id}")
def show_user(request: Request, id: str):
    db = next(get_db())

    users_query = db.query(models.User).filter(
        models.User.telegram_id == id).first()

    print(users_query)

    user_answers = [i[0] for i in db.query(models.Answer.content).filter(
        models.Answer.user_id == id
    ).all()]

    user_data = " ".join([
        "Username: ", users_query.username,
        "Email: ", users_query.email,
        "Answers: ", "; ".join(user_answers)
    ])

    main_translator = TranslatorI18n(app_language)
    context = {
        "request": request,
        "translator": main_translator,
        "user_name": users_query.username,
        "user_data": user_data
    }

    return templates.TemplateResponse("general_pages/show_user.html",
                                      context)
