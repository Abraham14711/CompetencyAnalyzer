from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..api import models, schemas
from competencyAnalyser.db.database import get_db

from random import sample

router = APIRouter()


def unpack(question):
    return question[0]


@router.get('/random_questions', response_model=List[schemas.QuestionOut])
def get_random_questions(vacancies: List[str], db: Session = Depends(get_db)):
    questions = [unpack(question) for question in db.query(models.Question).
                 filter(models.Question.vacancy.in_(vacancies)).all()]
    return sample(questions, 5)


def parse():
    with open("parsing/texts/to_parse.txt", 'r', encoding="utf-8") as file:
        examples = file.read()
        chunk = examples.split('&')
        for i in chunk:
            print(i.split("=")[0], end=";")


def flatten(xss):
    return [x for xs in xss for x in xs]


# def translate_list(list_to_translate: List[str], lang: str):
#     translator = Translator()
#     result = [translator.translate(word, dest=lang)
#        for word in list_to_translate]
#     return result
